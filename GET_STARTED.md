# 🚀 Get Started with Email Extractor

Welcome! This guide will get you up and running in 2 minutes.

## 🎨 Choose Your Interface

### Option 1: Web Interface (Recommended) ⭐

Beautiful, easy-to-use interface with drag-and-drop upload!

```bash
# Setup (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start the app
./start_app.sh
# OR
source venv/bin/activate && streamlit run app.py
```

Opens in your browser at `http://localhost:8501`

👉 **[Full Streamlit Guide](STREAMLIT_GUIDE.md)**

### Option 2: Command Line

Fast and scriptable for automation.

```bash
# Install
pip install --user --break-system-packages -r requirements.txt

# Use
python3 extract_emails.py sample_data.csv
```

---

## 📚 Documentation

- **[STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)** - Web interface guide (recommended!)
- **[README.md](README.md)** - Complete documentation with all features
- **[QUICKSTART.md](QUICKSTART.md)** - Common use cases and examples
- **[SUMMARY.md](SUMMARY.md)** - Project overview and technical details
- **[TEST_RESULTS.md](TEST_RESULTS.md)** - Comprehensive test results

---

## 🎯 Common Tasks

### Extract from CSV
```bash
python3 extract_emails.py data.csv
```

### Extract from Excel
```bash
python3 extract_emails.py workbook.xlsx
```

### Extract from Specific Columns
```bash
python3 extract_emails.py data.csv --columns "Email,Contact"
```

### Save Results to File
```bash
python3 extract_emails.py data.csv --out emails.txt
```

### Process Multiple Files
```bash
python3 extract_emails.py *.csv *.xlsx --out all_emails.txt
```

---

## 📋 Sample Data Included

Try the extractor with the included sample files:

**CSV File** (`sample_data.csv`):
- 5 contacts with email addresses
- Demonstrates extraction from multiple columns

**Excel File** (`sample_data.xlsx`):
- 3 sheets: Contacts, Vendors, Customers
- 11 unique email addresses

---

## 🔧 All Options

```bash
python3 extract_emails.py --help
```

| Option | Description |
|--------|-------------|
| `files` | Input files (.csv, .xlsx) |
| `--columns` | Specific columns to scan |
| `--sheets` | Excel sheets to process |
| `--delimiter` | Force CSV delimiter |
| `--out` | Save to file |
| `--no-header` | No header row |
| `--no-lower` | Keep original case |

---

## ✅ Features

- ✅ CSV and Excel support
- ✅ Auto-detect CSV delimiters
- ✅ Multi-sheet Excel processing
- ✅ Column filtering by name or index
- ✅ Email validation and normalization
- ✅ Automatic deduplication
- ✅ Batch processing multiple files

---

## 💡 Pro Tips

1. **Extract from all files in a directory**:
   ```bash
   python3 extract_emails.py *.csv *.xlsx --out all_emails.txt
   ```

2. **Process specific Excel sheets**:
   ```bash
   python3 extract_emails.py data.xlsx --sheets "Sheet1,Sheet2"
   ```

3. **Keep original email case**:
   ```bash
   python3 extract_emails.py data.csv --no-lower
   ```

4. **Handle semicolon-delimited CSV**:
   ```bash
   python3 extract_emails.py data.csv --delimiter ";"
   ```

---

## 🐛 Troubleshooting

### "python: command not found"
Use `python3` instead of `python`

### "openpyxl is required"
```bash
pip install --user --break-system-packages openpyxl
```

### "externally-managed-environment" error
Add `--user --break-system-packages` flags:
```bash
pip install --user --break-system-packages -r requirements.txt
```

---

## 📊 Example Output

```bash
$ python3 extract_emails.py sample_data.csv sample_data.xlsx

alice.williams@domain.co.uk
backup@corp.net
backup@test.com
bob@test.com
charlie@email.net
contact@abc-ind.com
david@globalservices.com
emily.chen@business.org
hello@123company.net
info@xyzcorp.com
jane.smith@company.org
john.doe@example.com
john@acme.com
lisa.brown@techsol.io
mike.davis@corp.net
sarah.j@company.com
tom.w@email.com
```

---

## 🎓 Learn More

- Read the full [README.md](README.md) for detailed documentation
- Check [TEST_RESULTS.md](TEST_RESULTS.md) to see all test cases
- Review [SUMMARY.md](SUMMARY.md) for technical details

---

## 📝 Need Help?

Run the help command to see all available options:
```bash
python3 extract_emails.py --help
```

---

**Ready to extract emails? Start with the sample data:**
```bash
python3 extract_emails.py sample_data.csv
```

Happy extracting! 🎉
