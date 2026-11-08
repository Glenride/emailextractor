# Email Extractor

A Python application to extract email addresses from CSV and XLSX spreadsheet files. Available as both a command-line tool and a beautiful web interface.

## 🎨 Two Ways to Use

### 1. Web Interface (Streamlit) - **Recommended**
Beautiful, easy-to-use web interface with drag-and-drop file upload, multiple view modes, and easy copying.

```bash
source venv/bin/activate
streamlit run app.py
```

👉 **[See Streamlit Guide](STREAMLIT_GUIDE.md)** for detailed instructions

### 2. Command Line
Powerful CLI for automation and scripting.

```bash
python3 extract_emails.py data.csv --out emails.txt
```

## Features

- **🎨 Web Interface**: Drag-and-drop upload, multiple view modes, easy copying
- **💻 Command Line**: Powerful CLI for automation
- **Multiple file format support**: CSV, XLSX, XLSM
- **Flexible column selection**: Extract from specific columns by name or index
- **Smart CSV detection**: Automatically detects delimiters (comma, semicolon, tab, pipe)
- **Excel sheet selection**: Process specific sheets or all sheets
- **Email validation**: Filters out malformed email addresses
- **Deduplication**: Automatically removes duplicate emails
- **Case normalization**: Optionally lowercase all emails
- **Multiple export formats**: TXT, CSV, comma-separated, semicolon-separated

## Installation

### Option 1: Virtual Environment (Recommended for Web Interface)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option 2: User Install (For Command Line Only)

```bash
pip install --user --break-system-packages -r requirements.txt
```

**Note**: The web interface requires a virtual environment for best compatibility.

## Usage

### Basic Usage

Extract emails from all columns in a CSV file:

```bash
python3 extract_emails.py data.csv
```

Extract emails from multiple files:

```bash
python3 extract_emails.py file1.csv file2.xlsx file3.csv
```

### Column Selection

Extract from specific columns by name:

```bash
python3 extract_emails.py data.csv --columns "Email,Contact Email"
```

Extract from specific columns by index (1-based):

```bash
python3 extract_emails.py data.csv --columns "2,5,7"
```

Mix column names and indices:

```bash
python3 extract_emails.py data.xlsx --columns "Email,3,Contact"
```

### Excel Options

Process specific sheets:

```bash
python3 extract_emails.py workbook.xlsx --sheets "Sheet1,Contacts"
```

Process sheets by index (1-based):

```bash
python3 extract_emails.py workbook.xlsx --sheets "1,3"
```

### CSV Options

Force a specific delimiter:

```bash
python3 extract_emails.py data.csv --delimiter ";"
```

Use tab delimiter:

```bash
python3 extract_emails.py data.csv --delimiter $'\t'
```

### Output Options

Save results to a file:

```bash
python3 extract_emails.py data.csv --out emails.txt
```

Preserve original case (don't lowercase):

```bash
python3 extract_emails.py data.csv --no-lower
```

### Advanced Options

Treat first row as data (no header):

```bash
python3 extract_emails.py data.csv --no-header --columns "1,3"
```

## Examples

### Example 1: Extract from CSV with header

```bash
python3 extract_emails.py contacts.csv --columns "Email Address" --out results.txt
```

### Example 2: Extract from multiple Excel sheets

```bash
python3 extract_emails.py company_data.xlsx --sheets "Employees,Customers" --out all_emails.txt
```

### Example 3: Process semicolon-delimited CSV

```bash
python3 extract_emails.py european_data.csv --delimiter ";" --columns "Email,Backup Email"
```

### Example 4: Extract from all files in directory

```bash
python3 extract_emails.py *.csv *.xlsx --out combined_emails.txt
```

## Email Validation

The script performs the following validation:

- Matches standard email format: `username@domain.tld`
- Removes surrounding punctuation and whitespace
- Filters out emails with invalid domain formats
- Requires at least one dot in the domain
- Removes trailing sentence punctuation

## Technology Stack

- **Python 3.7+**: Core language
- **openpyxl**: Excel file processing
- **csv**: CSV file processing (built-in)
- **argparse**: Command-line interface (built-in)
- **re**: Regular expression matching (built-in)

## Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `files` | Input files (.csv, .xlsx) | Required |
| `--columns` | Column names or indices to scan | All columns |
| `--no-header` | Treat first row as data | False |
| `--sheets` | Sheet names or indices (Excel only) | All sheets |
| `--delimiter` | Force CSV delimiter | Auto-detect |
| `--out` | Output file path | stdout |
| `--allow-duplicates` | Don't deduplicate emails | False |
| `--no-lower` | Don't lowercase emails | False |

## Error Handling

- Missing files generate warnings but don't stop processing
- Unsupported file types are skipped with a warning
- Processing errors for individual files are reported but don't halt execution
- Missing openpyxl dependency provides clear installation instructions

## License

This script is provided as-is for email extraction purposes.
