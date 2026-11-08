import streamlit as st
import pandas as pd
import io
from pathlib import Path
import sys

# Import the extraction functions from extract_emails.py
from extract_emails import (
    extract_emails_from_text,
    process_csv,
    process_xlsx,
    normalize_email
)

st.set_page_config(
    page_title="Email Extractor",
    page_icon="📧",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .email-box {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        font-family: monospace;
        max-height: 400px;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("📧 Email Extractor")
st.markdown("Extract email addresses from CSV and Excel files with ease!")

# Initialize session state
if 'extracted_emails' not in st.session_state:
    st.session_state.extracted_emails = set()
if 'email_sources' not in st.session_state:
    st.session_state.email_sources = {}

# Sidebar for options
with st.sidebar:
    st.header("⚙️ Options")
    
    lowercase_emails = st.checkbox("Lowercase emails", value=True)
    show_duplicates = st.checkbox("Show duplicates", value=False)
    
    st.divider()
    
    st.header("📊 Statistics")
    if st.session_state.extracted_emails:
        st.metric("Total Emails", len(st.session_state.extracted_emails))
        
        # Show domain statistics
        domains = {}
        for email in st.session_state.extracted_emails:
            domain = email.split('@')[1] if '@' in email else 'unknown'
            domains[domain] = domains.get(domain, 0) + 1
        
        st.subheader("Top Domains")
        for domain, count in sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]:
            st.text(f"{domain}: {count}")

# Main content area
tab1, tab2, tab3 = st.tabs(["📁 Upload Files", "📋 View Results", "ℹ️ Help"])

with tab1:
    st.header("Upload Your Files")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose CSV or Excel files",
        type=['csv', 'xlsx', 'xlsm'],
        accept_multiple_files=True,
        help="Upload one or more CSV or Excel files"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Column selection
        column_input = st.text_input(
            "Columns to scan (optional)",
            placeholder="e.g., Email, Contact, or leave blank for all",
            help="Comma-separated column names or indices. Leave blank to scan all columns."
        )
    
    with col2:
        # Sheet selection for Excel
        sheet_input = st.text_input(
            "Excel sheets (optional)",
            placeholder="e.g., Sheet1, Contacts, or leave blank for all",
            help="Comma-separated sheet names or indices. Only applies to Excel files."
        )
    
    # Process button
    if st.button("🔍 Extract Emails", type="primary", disabled=not uploaded_files):
        with st.spinner("Extracting emails..."):
            # Clear previous results
            st.session_state.extracted_emails = set()
            st.session_state.email_sources = {}
            
            # Parse column and sheet inputs
            columns = [c.strip() for c in column_input.split(',') if c.strip()] if column_input else []
            sheets = [s.strip() for s in sheet_input.split(',') if s.strip()] if sheet_input else []
            
            # Process each file
            for uploaded_file in uploaded_files:
                try:
                    file_emails = set()
                    suffix = Path(uploaded_file.name).suffix.lower()
                    
                    if suffix == '.csv':
                        # Save uploaded file temporarily
                        temp_path = Path(f"/tmp/{uploaded_file.name}")
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())
                        
                        process_csv(temp_path, file_emails, columns, no_header=False, delimiter=None)
                        temp_path.unlink()  # Clean up
                        
                    elif suffix in ['.xlsx', '.xlsm']:
                        # Save uploaded file temporarily
                        temp_path = Path(f"/tmp/{uploaded_file.name}")
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getvalue())
                        
                        process_xlsx(temp_path, file_emails, columns, no_header=False, sheets=sheets)
                        temp_path.unlink()  # Clean up
                    
                    # Store source information
                    for email in file_emails:
                        if email not in st.session_state.email_sources:
                            st.session_state.email_sources[email] = []
                        st.session_state.email_sources[email].append(uploaded_file.name)
                    
                    st.session_state.extracted_emails.update(file_emails)
                    
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            if st.session_state.extracted_emails:
                st.success(f"✅ Extracted {len(st.session_state.extracted_emails)} unique emails!")
                st.balloons()
            else:
                st.warning("No emails found in the uploaded files.")

with tab2:
    st.header("Extracted Emails")
    
    if st.session_state.extracted_emails:
        # Sort emails
        emails_list = sorted(st.session_state.extracted_emails)
        
        # Apply lowercase if needed
        if not lowercase_emails:
            emails_list = [normalize_email(e, to_lower=False) for e in emails_list]
        
        # Create columns for actions
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Copy all emails button (creates a text area with all emails)
            all_emails_text = '\n'.join(emails_list)
            st.download_button(
                label="📥 Download as TXT",
                data=all_emails_text,
                file_name="extracted_emails.txt",
                mime="text/plain"
            )
        
        with col2:
            # Download as CSV
            df = pd.DataFrame({'Email': emails_list})
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name="extracted_emails.csv",
                mime="text/csv"
            )
        
        with col3:
            # Copy comma-separated
            comma_separated = ', '.join(emails_list)
            st.download_button(
                label="📥 Comma-Separated",
                data=comma_separated,
                file_name="emails_comma_separated.txt",
                mime="text/plain"
            )
        
        with col4:
            # Clear results
            if st.button("🗑️ Clear Results"):
                st.session_state.extracted_emails = set()
                st.session_state.email_sources = {}
                st.rerun()
        
        st.divider()
        
        # Display options
        display_option = st.radio(
            "Display format:",
            ["List View", "Table View", "Copy Box"],
            horizontal=True
        )
        
        if display_option == "List View":
            # Show emails in a scrollable list with source info
            st.subheader(f"📋 {len(emails_list)} Emails Found")
            
            # Search/filter
            search = st.text_input("🔍 Search emails", placeholder="Type to filter...")
            
            if search:
                filtered_emails = [e for e in emails_list if search.lower() in e.lower()]
            else:
                filtered_emails = emails_list
            
            # Display with expanders showing source
            for i, email in enumerate(filtered_emails, 1):
                with st.expander(f"{i}. {email}"):
                    sources = st.session_state.email_sources.get(email, ['Unknown'])
                    st.write(f"**Found in:** {', '.join(sources)}")
                    st.code(email, language=None)
        
        elif display_option == "Table View":
            # Create DataFrame with source information
            data = []
            for email in emails_list:
                sources = st.session_state.email_sources.get(email, ['Unknown'])
                data.append({
                    'Email': email,
                    'Domain': email.split('@')[1] if '@' in email else 'N/A',
                    'Source Files': ', '.join(sources)
                })
            
            df = pd.DataFrame(data)
            
            # Add search
            search = st.text_input("🔍 Search emails", placeholder="Type to filter...")
            if search:
                df = df[df['Email'].str.contains(search, case=False, na=False)]
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Email": st.column_config.TextColumn("Email Address", width="large"),
                    "Domain": st.column_config.TextColumn("Domain", width="medium"),
                    "Source Files": st.column_config.TextColumn("Source", width="medium")
                }
            )
        
        else:  # Copy Box
            st.subheader("📋 Copy Emails")
            st.info("Select the text below and copy (Cmd+C or Ctrl+C)")
            
            # Create a text area with all emails for easy copying
            st.text_area(
                "All emails (one per line)",
                value=all_emails_text,
                height=300,
                help="Click inside and press Cmd+A (Mac) or Ctrl+A (Windows) to select all, then Cmd+C or Ctrl+C to copy"
            )
            
            # Also show comma-separated version
            st.text_area(
                "Comma-separated emails",
                value=comma_separated,
                height=100,
                help="Useful for pasting into email clients"
            )
            
            # Show semicolon-separated (useful for some applications)
            semicolon_separated = '; '.join(emails_list)
            st.text_area(
                "Semicolon-separated emails",
                value=semicolon_separated,
                height=100,
                help="Useful for some CRM systems"
            )
    
    else:
        st.info("👆 Upload files in the 'Upload Files' tab to get started!")
        
        # Show example
        st.subheader("Example Output")
        st.code("""john.doe@example.com
jane.smith@company.org
bob@test.com
alice.williams@domain.co.uk""", language=None)

with tab3:
    st.header("📖 How to Use")
    
    st.markdown("""
    ### Step 1: Upload Files
    1. Go to the **Upload Files** tab
    2. Click "Browse files" or drag and drop your CSV/Excel files
    3. (Optional) Specify columns or sheets to scan
    4. Click **Extract Emails**
    
    ### Step 2: View Results
    1. Switch to the **View Results** tab
    2. Choose your preferred display format:
       - **List View**: Expandable list with source information
       - **Table View**: Sortable table with domains
       - **Copy Box**: Text areas for easy copying
    
    ### Step 3: Export or Copy
    - **Download as TXT**: One email per line
    - **Download as CSV**: Spreadsheet format
    - **Comma-Separated**: For email clients
    - **Copy directly**: Select text and copy (Cmd+C / Ctrl+C)
    
    ### Supported File Types
    - ✅ CSV files (.csv)
    - ✅ Excel files (.xlsx, .xlsm)
    - ✅ Multiple files at once
    
    ### Features
    - 🔍 Smart email detection and validation
    - 🎯 Column and sheet filtering
    - 📊 Domain statistics
    - 🔄 Automatic deduplication
    - 📋 Multiple export formats
    - 🔎 Search and filter results
    
    ### Tips
    - Leave column/sheet fields blank to scan everything
    - Use the search box to quickly find specific emails
    - Check the sidebar for statistics about your extracted emails
    - Download in different formats depending on your needs
    """)
    
    st.divider()
    
    st.subheader("🐛 Troubleshooting")
    st.markdown("""
    - **No emails found?** Make sure your files contain valid email addresses
    - **Wrong columns?** Specify column names in the "Columns to scan" field
    - **Excel issues?** Make sure openpyxl is installed: `pip install openpyxl`
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📧 Email Extractor | Built with Streamlit</p>
    <p><small>Upload your files, extract emails, and copy them easily!</small></p>
</div>
""", unsafe_allow_html=True)
