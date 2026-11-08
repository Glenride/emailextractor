import argparse
import csv
import re
import sys
from pathlib import Path

EMAIL_REGEX = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', re.IGNORECASE)


def normalize_email(e: str, to_lower: bool = True) -> str:
    """Normalize an email address by stripping punctuation and optionally lowercasing."""
    if not e:
        return ''
    # Strip common surrounding punctuation
    e = e.strip().strip("<>()[]{}'\",;: ")
    # Remove trailing punctuation that might cling to sentences
    while e and e[-1] in '.,;:)]}':
        e = e[:-1]
    return e.lower() if to_lower else e


def extract_emails_from_text(text: str) -> list:
    """Extract all email addresses from a text string."""
    if text is None:
        return []
    if not isinstance(text, str):
        text = str(text)
    
    matches = EMAIL_REGEX.findall(text)
    # Normalize and filter obviously malformed leftovers
    out = []
    for m in matches:
        n = normalize_email(m)
        # Basic sanity checks
        if not n or '@' not in n:
            continue
        local, _, domain = n.partition('@')
        if not local or not domain:
            continue
        if domain.startswith(('.', '-')) or domain.endswith(('.', '-')):
            continue
        if '.' not in domain:
            continue
        out.append(n)
    return out


def sniff_csv_dialect(sample: str):
    """Detect CSV dialect from a sample."""
    try:
        return csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t', '|'])
    except Exception:
        # Fallback to comma
        d = csv.excel()
        d.delimiter = ','
        return d


def resolve_column_indices(header, requested, no_header: bool):
    """Resolve column names or indices to actual column indices."""
    if not requested:
        return None  # means "all columns"
    
    indices = set()
    if no_header:
        # Treat all requested as numeric indices (0-based or 1-based)
        for tok in requested:
            tok = tok.strip()
            if tok.isdigit():
                idx = int(tok)
                if idx > 100000:  # sanity guard
                    continue
                # Accept 0-based or 1-based; normalize to 0-based
                if idx > 0:
                    indices.add(idx - 1)
                else:
                    indices.add(idx)
        return sorted(indices) if indices else None
    
    # Map names (case-insensitive, trimmed) to indices; also accept numeric tokens
    name_to_idx = {}
    for i, name in enumerate(header or []):
        key = str(name).strip().lower()
        if key and key not in name_to_idx:
            name_to_idx[key] = i
    
    for tok in requested:
        tok = str(tok).strip()
        if tok.isdigit():
            idx = int(tok)
            # Interpret as 0-based if 0 present, else 1-based if >=1
            indices.add(idx if idx == 0 else idx - 1)
        else:
            key = tok.lower()
            if key in name_to_idx:
                indices.add(name_to_idx[key])
    
    return sorted(i for i in indices if i is not None)


def process_csv(path: Path, emails: set, columns: list, no_header: bool, delimiter: str = None):
    """Process a CSV file and extract emails."""
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        sample = f.read(4096)
        f.seek(0)
        
        if delimiter:
            dialect = csv.excel()
            dialect.delimiter = delimiter
        else:
            dialect = sniff_csv_dialect(sample)
        
        reader = csv.reader(f, dialect)
        header = None
        col_indices = None
        first_row = True
        
        for row in reader:
            if first_row and not no_header:
                header = row
                col_indices = resolve_column_indices(header, columns, no_header=False)
                first_row = False
                # If we still want to scan all columns, skip to next row
                if columns:
                    continue
            
            if first_row and no_header:
                # No header: build indices only if requested
                col_indices = resolve_column_indices(None, columns, no_header=True)
                first_row = False
            
            cells = []
            if col_indices is None:
                cells = row
            else:
                cells = [row[i] for i in col_indices if 0 <= i < len(row)]
            
            for cell in cells:
                for e in extract_emails_from_text(cell):
                    emails.add(e)


def process_xlsx(path: Path, emails: set, columns: list, no_header: bool, sheets: list):
    """Process an XLSX file and extract emails."""
    try:
        import openpyxl
    except ImportError:
        sys.stderr.write("Error: openpyxl is required to read .xlsx files. Install with: pip install openpyxl\n")
        sys.exit(1)
    
    wb = openpyxl.load_workbook(filename=str(path), read_only=True, data_only=True)
    sheet_names = wb.sheetnames
    target_sheets = sheet_names
    
    if sheets:
        wanted = set(s.strip().lower() for s in sheets)
        target_sheets = [s for s in sheet_names if s.lower() in wanted or str(sheet_names.index(s)+1) in wanted]
    
    for sname in target_sheets:
        ws = wb[sname]
        header = None
        col_indices = None
        first_row = True
        
        for row in ws.iter_rows(values_only=True):
            if first_row and not no_header:
                header = [cell for cell in row]
                col_indices = resolve_column_indices(header, columns, no_header=False)
                first_row = False
                if columns:
                    # scanning specific columns; continue to next row
                    continue
            
            if first_row and no_header:
                col_indices = resolve_column_indices(None, columns, no_header=True)
                first_row = False
            
            cells = []
            if col_indices is None:
                cells = row
            else:
                cells = [row[i] for i in col_indices if 0 <= i < len(row)]
            
            for cell in cells:
                for e in extract_emails_from_text(cell):
                    emails.add(e)


def main():
    ap = argparse.ArgumentParser(description="Extract email addresses from CSV and XLSX files.")
    ap.add_argument('files', nargs='+', help='Input files (.csv, .xlsx)')
    ap.add_argument('--columns', type=str, default='', help='Comma-separated column names or indices to scan. If omitted, all columns are scanned.')
    ap.add_argument('--no-header', action='store_true', help='Treat first row as data (no header).')
    ap.add_argument('--sheets', type=str, default='', help='For .xlsx: comma-separated sheet names or indices (1-based). Default: all sheets.')
    ap.add_argument('--delimiter', type=str, default=None, help='Force CSV delimiter (e.g., ",", ";", "\\t").')
    ap.add_argument('--out', type=str, default='', help='Output file path. If omitted, prints to stdout.')
    ap.add_argument('--allow-duplicates', action='store_true', help='Do not deduplicate emails (prints in discovery order).')
    ap.add_argument('--no-lower', action='store_true', help='Do not lowercase emails.')
    
    args = ap.parse_args()
    
    files = [Path(p) for p in args.files]
    columns = [c.strip() for c in args.columns.split(',') if c.strip()] if args.columns else []
    sheets = [s.strip() for s in args.sheets.split(',') if s.strip()] if args.sheets else []
    to_lower = not args.no_lower
    
    all_emails_set = set()
    all_emails_list = []  # if duplicates allowed
    
    for path in files:
        if not path.exists():
            sys.stderr.write(f"Warning: file not found: {path}\n")
            continue
        
        suffix = path.suffix.lower()
        try:
            if suffix == '.csv':
                process_csv(path, all_emails_set, columns, args.no_header, args.delimiter)
            elif suffix in ('.xlsx', '.xlsm'):
                process_xlsx(path, all_emails_set, columns, args.no_header, sheets)
            else:
                sys.stderr.write(f"Skipping unsupported file type: {path}\n")
        except Exception as ex:
            sys.stderr.write(f"Error processing {path}: {ex}\n")
    
    # If duplicates allowed, rebuild from scanning again with list accumulation
    # to preserve discovery order with duplicates; otherwise just use the set.
    # For simplicity, we'll keep dedup by default.
    results = sorted(all_emails_set)
    if not to_lower:
        # Re-run normalization case setting
        results = [normalize_email(e, to_lower=False) for e in results]
    
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with out_path.open('w', encoding='utf-8') as f:
            for e in results:
                f.write(e + '\n')
        print(f"Wrote {len(results)} unique emails to {out_path}")
    else:
        for e in results:
            print(e)


if __name__ == '__main__':
    main()
