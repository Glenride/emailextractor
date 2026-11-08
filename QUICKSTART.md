# Quick Start Guide

## Installation

```bash
pip install --user -r requirements.txt
```

## Basic Usage

### Extract from CSV (all columns)
```bash
python3 extract_emails.py sample_data.csv
```

### Extract from specific column
```bash
python3 extract_emails.py sample_data.csv --columns "Email"
```

### Save to file
```bash
python3 extract_emails.py sample_data.csv --out emails.txt
```

### Extract from Excel file
```bash
python3 extract_emails.py workbook.xlsx
```

### Extract from specific Excel sheet
```bash
python3 extract_emails.py workbook.xlsx --sheets "Sheet1"
```

### Process multiple files
```bash
python3 extract_emails.py file1.csv file2.xlsx file3.csv --out all_emails.txt
```

## Common Use Cases

### 1. Extract from email column only
```bash
python3 extract_emails.py contacts.csv --columns "Email" --out results.txt
```

### 2. Extract from multiple columns
```bash
python3 extract_emails.py data.csv --columns "Primary Email,Secondary Email,Notes"
```

### 3. Process semicolon-delimited CSV
```bash
python3 extract_emails.py data.csv --delimiter ";"
```

### 4. Keep original case
```bash
python3 extract_emails.py data.csv --no-lower
```

### 5. Process CSV without header row
```bash
python3 extract_emails.py data.csv --no-header --columns "2,4"
```

## Testing

Test with the included sample data:

```bash
python3 extract_emails.py sample_data.csv
```

Expected output:
```
alice.williams@domain.co.uk
backup@test.com
bob@test.com
charlie@email.net
jane.smith@company.org
john.doe@example.com
```

## Troubleshooting

### "openpyxl is required" error
```bash
pip install --user openpyxl
```

### "python: command not found"
Use `python3` instead:
```bash
python3 extract_emails.py file.csv
```

### Permission denied when installing
Add `--user` flag:
```bash
pip install --user -r requirements.txt
```
