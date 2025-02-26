import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure the Streamlit app's appearance and layout
# 'page_title' sets the browser tab title
# 'layout="wide"' allows more horizontal space, improving the display for tables and graphs
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for styling the app with dark mode aesthetics
# This enhances the UI by setting background colors, button styles, and text formatting
st.markdown(
    """
    <style>
    /* Overall Page Styling */
    .main {
        background-color: #121212;
        font-family: 'Poppins', sans-serif;  /* Modern Font */
    }

    /* Main Container */
    .block-container {
        padding: 3rem;
        border-radius: 15px;
        background-color: #1e1e1e;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.1); /* Softer Shadow */
        transition: all 0.3s ease-in-out;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #66c2ff;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Buttons */
    .stButton>button {
        border: none;
        border-radius: 10px;
        background: linear-gradient(135deg, #0078D7, #005a9e);
        color: white;
        padding: 12px 20px;
        font-size: 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 10px rgba(0, 120, 215, 0.5);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #005a9e, #003f7f);
        transform: scale(1.05);
        cursor: pointer;
    }

    /* Tables & Data Frames */
    .stDataFrame, .stTable {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.2);
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
    }

    /* Radio & Checkboxes */
    .stRadio>label, .stCheckbox>label {
        font-weight: bold;
        color: white;
    }

    /* Download Button */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745, #218838);
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 18px;
        transition: 0.3s ease-in-out;
    }

    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #218838, #1e7e34);
        transform: scale(1.05);
    }
 </style>
        """,
    unsafe_allow_html=True  # 'unsafe_allow_html' permits raw HTML/CSS embedding in the Streamlit app
)

# Display the main app title and introductory text
st.title("💿Advanced Data Sweeper")  # Large, eye-catching title
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader widget that accepts CSV and Excel files
# 'accept_multiple_files=True' allows batch uploading multiple files at once
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Processing logic for uploaded files (if any files are uploaded)
if uploaded_files:
    for file in uploaded_files:
        # Extract the file extension to determine if it's CSV or Excel
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        # Read the uploaded file into a pandas DataFrame based on its extension
        if file_extension == ".csv":
            df = pd.read_csv(file)  # Read CSV files
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)  # Read Excel files
        else:
            # Show an error message if the file type is unsupported
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        # Display uploaded file information (name and size)
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB

        # Preview the first 5 rows of the uploaded file
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())  # Display a scrollable preview of the data
        
        # Section for data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)  # Split cleaning options into two columns
            with col1:
                # Button to remove duplicate rows from the DataFrame
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
            with col2:
                # Button to fill missing numeric values with column means
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values in Numeric Columns Filled with Column Means!")

        # Section to choose specific columns to convert
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]  # Filters the DataFrame to the selected columns
        
        # Visualization section for uploaded data
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])  # Plot the first two numeric columns as a bar chart
        
        # Section to choose file conversion type (CSV or Excel)
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()  # Creates in-memory buffer for file output
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  # Save DataFrame as CSV in buffer
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')  # Save as Excel using openpyxl
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            
            # Download button for the converted file
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")  # Display success message when all files are processed


