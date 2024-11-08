import streamlit as st
import camelot
import pandas as pd
from io import BytesIO
import os

# Function to extract tables and return a dictionary of DataFrames
def extract_tables_from_pdf(file_path):
    tables_dict = {}
    try:
        # Read tables from the PDF
        tables = camelot.read_pdf(file_path, pages='all', flavor='stream')

        # Iterate through the tables and store them in the dictionary
        for i, table in enumerate(tables):
            df = table.df
            df['Page Number'] = table.page
            tables_dict[f'Table {i + 1}'] = df
        return tables_dict

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app
def main():
    # Custom CSS for background color and title
    st.markdown("""
        <style>
            .main {
                background-color: orange;
            }
            .title-container {
                display: flex;
                align-items: center;
                justify-content: left;
                background-color: orange;
                padding: 10px;
            }
            .title-container img {
                margin-right: 20px;
                height: 80px;  /* Adjust logo height */
            }
            .title-container h1 {
                color: white;
                font-size: 36px;
                margin: 0;
            }
        </style>
        """, unsafe_allow_html=True)

    # Logo and title container with orange background
    st.markdown('<div class="title-container">', unsafe_allow_html=True)
    st.image("https://enoahisolution.com/wp-content/themes/enoah-new/images/newimages/enoah-logo-fixed.png", width=80)  # Replace with your logo path
    st.markdown('<h1>PDF Table Extractor</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Upload PDF file
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file is not None:
        # Save the uploaded PDF to a temporary location
        file_name = uploaded_file.name
        file_path = f'/tmp/{file_name}'
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Automatically trigger the extraction after the file is uploaded
        tables_dict = extract_tables_from_pdf(file_path)

        if tables_dict:
            # Create an Excel file in memory
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                for table_name, df in tables_dict.items():
                    df.to_excel(writer, sheet_name=table_name, index=False)

            # Prepare download of the Excel file with the same name as the uploaded PDF
            output.seek(0)
            st.download_button(
                label="Download Tables as Excel",
                data=output,
                file_name=f"{os.path.splitext(file_name)[0]}.xlsx",  # Same name as the PDF but with .xlsx extension
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()
