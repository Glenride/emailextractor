# 🎨 Streamlit Web Interface Guide

## Overview

The Email Extractor now includes a beautiful web interface built with Streamlit that makes it easy to upload files, view extracted emails, and copy them to other programs.

## 🚀 Quick Start

### 1. Install Dependencies (First Time Only)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the App

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Run the app
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

### 3. Stop the App

Press `Ctrl+C` in the terminal to stop the server.

---

## 📋 Features

### 🎯 Main Features

- **📁 File Upload**: Drag and drop or browse for CSV/Excel files
- **🔍 Smart Extraction**: Automatically detects and validates emails
- **📊 Statistics Dashboard**: View email counts and domain statistics
- **🎨 Multiple View Modes**: List, Table, or Copy Box views
- **📥 Multiple Export Formats**: TXT, CSV, comma-separated, semicolon-separated
- **🔎 Search & Filter**: Quickly find specific emails
- **📋 Easy Copying**: Select and copy emails directly from the interface

### 🎨 Interface Sections

#### 1. Upload Files Tab
- Upload multiple CSV or Excel files at once
- Optional column filtering (e.g., "Email, Contact")
- Optional sheet selection for Excel files (e.g., "Sheet1, Contacts")
- Extract button to process files

#### 2. View Results Tab
- **List View**: Expandable list showing source file for each email
- **Table View**: Sortable table with email, domain, and source columns
- **Copy Box**: Text areas with different formats for easy copying

#### 3. Help Tab
- Step-by-step instructions
- Troubleshooting tips
- Feature overview

#### 4. Sidebar
- Email count statistics
- Top domains breakdown
- Options for lowercase and duplicates

---

## 🎯 How to Use

### Basic Workflow

1. **Upload Files**
   - Go to "Upload Files" tab
   - Click "Browse files" or drag & drop your files
   - Click "Extract Emails" button

2. **View Results**
   - Switch to "View Results" tab
   - Choose your preferred display format
   - Use search to filter results

3. **Copy or Export**
   - **Copy directly**: Select text and press Cmd+C (Mac) or Ctrl+C (Windows)
   - **Download**: Click download buttons for different formats
   - **Paste**: Paste into your target application

---

## 📥 Export Options

### 1. Download as TXT
- One email per line
- Perfect for importing into email lists
- Clean, simple format

### 2. Download as CSV
- Spreadsheet format
- Can be opened in Excel or Google Sheets
- Includes header row

### 3. Comma-Separated
- All emails in one line, separated by commas
- Perfect for email clients (To/CC/BCC fields)
- Example: `email1@test.com, email2@test.com`

### 4. Semicolon-Separated
- All emails in one line, separated by semicolons
- Useful for some CRM systems
- Example: `email1@test.com; email2@test.com`

---

## 💡 Pro Tips

### Copying Emails

**Method 1: Copy Box View**
1. Switch to "Copy Box" display format
2. Click inside the text area
3. Press Cmd+A (Mac) or Ctrl+A (Windows) to select all
4. Press Cmd+C (Mac) or Ctrl+C (Windows) to copy
5. Paste into your target application

**Method 2: Direct Selection**
1. Use any view mode
2. Click and drag to select emails
3. Press Cmd+C or Ctrl+C to copy

**Method 3: Download Button**
1. Click the appropriate download button
2. Open the downloaded file
3. Copy from there

### Column Filtering

To extract emails from specific columns:
```
Email, Contact Email, Notes
```

Or use column indices (1-based):
```
2, 5, 7
```

### Excel Sheet Selection

To process specific sheets:
```
Contacts, Vendors, Customers
```

Or use sheet indices (1-based):
```
1, 3, 5
```

### Search & Filter

- Use the search box to quickly find specific emails
- Search is case-insensitive
- Works across all view modes

---

## 🎨 View Modes Explained

### List View
- **Best for**: Reviewing emails one by one
- **Features**: 
  - Expandable items showing source file
  - Easy to scan through results
  - Shows which file each email came from

### Table View
- **Best for**: Analyzing data
- **Features**:
  - Sortable columns
  - Shows email, domain, and source
  - Easy to compare and analyze

### Copy Box
- **Best for**: Copying emails to other programs
- **Features**:
  - Three different formats (line-separated, comma-separated, semicolon-separated)
  - Easy selection and copying
  - No extra formatting to deal with

---

## 🔧 Advanced Usage

### Processing Multiple Files

1. Upload multiple CSV and Excel files at once
2. The app will combine and deduplicate all emails
3. View statistics to see total count
4. Source information shows which files contained each email

### Column-Specific Extraction

1. Enter column names in "Columns to scan" field
2. Use exact column names (case-insensitive)
3. Separate multiple columns with commas
4. Leave blank to scan all columns

### Excel Multi-Sheet Processing

1. Enter sheet names in "Excel sheets" field
2. Use exact sheet names or indices
3. Separate multiple sheets with commas
4. Leave blank to process all sheets

---

## 🐛 Troubleshooting

### App Won't Start

**Problem**: `streamlit: command not found`

**Solution**:
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Verify streamlit is installed
pip list | grep streamlit

# If not installed
pip install streamlit
```

### No Emails Found

**Problem**: Uploaded files but no emails extracted

**Solutions**:
- Check that your files contain valid email addresses
- Try leaving column/sheet fields blank to scan everything
- Verify file format is CSV or Excel (.xlsx, .xlsm)

### Can't Copy Emails

**Problem**: Copy function not working

**Solutions**:
- Use the "Copy Box" view mode
- Click inside the text area first
- Try using download buttons instead
- Check browser permissions for clipboard access

### Upload Failed

**Problem**: File upload errors

**Solutions**:
- Check file size (very large files may take time)
- Verify file format (.csv, .xlsx, .xlsm)
- Try uploading files one at a time
- Check that files aren't corrupted

---

## 🎯 Use Cases

### 1. Email Marketing Lists
1. Upload customer database (CSV/Excel)
2. Extract emails from "Email" column
3. Download as comma-separated
4. Paste into email marketing tool

### 2. Contact Management
1. Upload multiple contact lists
2. Extract all emails (scans all columns)
3. View in Table mode to see domains
4. Download as CSV for import into CRM

### 3. Data Cleaning
1. Upload messy spreadsheet
2. Let the app validate and clean emails
3. View statistics to see results
4. Download cleaned list

### 4. Multi-Source Consolidation
1. Upload files from different sources
2. App automatically deduplicates
3. View which files contained each email
4. Export consolidated list

---

## ⌨️ Keyboard Shortcuts

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Select All | Cmd+A | Ctrl+A |
| Copy | Cmd+C | Ctrl+C |
| Paste | Cmd+V | Ctrl+V |
| Find | Cmd+F | Ctrl+F |
| Refresh Page | Cmd+R | Ctrl+R |

---

## 📊 Statistics Sidebar

The sidebar shows:
- **Total Emails**: Count of unique emails extracted
- **Top Domains**: Most common email domains
- **Options**: Toggle lowercase and duplicate handling

---

## 🎨 Interface Tips

### Better Performance
- Process files one at a time if they're very large
- Use column filtering to reduce processing time
- Clear results before processing new files

### Better Organization
- Use Table View to sort by domain
- Use List View to see source files
- Use search to find specific emails quickly

### Better Copying
- Use Copy Box for bulk copying
- Use comma-separated for email clients
- Use semicolon-separated for CRM systems
- Download as CSV for spreadsheet programs

---

## 🔄 Workflow Examples

### Example 1: Quick Email List

```
1. Upload file → 2. Click Extract → 3. Copy Box → 4. Select All → 5. Copy
```

### Example 2: Filtered Extraction

```
1. Upload file → 2. Enter "Email" in columns → 3. Extract → 4. Download CSV
```

### Example 3: Multi-File Consolidation

```
1. Upload multiple files → 2. Extract → 3. View Table → 4. Download TXT
```

---

## 🚀 Starting the App (Quick Reference)

```bash
# Navigate to project directory
cd /path/to/emailextractor

# Activate virtual environment
source venv/bin/activate

# Start the app
streamlit run app.py

# Open browser to: http://localhost:8501
```

---

## 📝 Notes

- The app runs locally on your computer
- Files are processed in memory (not saved to disk)
- All data stays on your machine (no cloud upload)
- Close the browser tab when done
- Press Ctrl+C in terminal to stop the server

---

## 🎉 Enjoy!

The Streamlit interface makes email extraction fast, easy, and visual. Upload your files, view the results, and copy emails with just a few clicks!

**Need help?** Check the Help tab in the app or refer to the main README.md.
