import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Data Sweeper", layout="wide", page_icon="🧹")

# Custom CSS
st.markdown(
	"""
	<style>
	.stApp{
		background-color: black;
		color: white;
	}
	</style>
	""",
	unsafe_allow_html=True
)

# Title and description
st.title("💿 Data Sweeper")
st.write("A simple tool to clean and visualize your data")
st.write("Transform your data into a clean and readable format with Data Sweeper. Upload your data and get started!")

# File uploader
uploaded_files = st.file_uploader("Upload your CSV and Excel files", type=[
								  "csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
	for file in uploaded_files:
		file_ext = os.path.splitext(file.name)[-1].lower()

		if file_ext == ".csv":
			df = pd.read_csv(file)
		elif file_ext == ".xlsx":
			df = pd.read_excel(file)
		else:
			st.error(f"{file_ext} file type is not supported")
			continue

		# file details
		st.write("🔍 Preview the head of the DataFrame")
		st.dataframe(df.head())

		# data cleaning options
		st.subheader("🧼 Data Cleaning Options")
		if st.checkbox(f"clean data for {file.name}"):
			col1, col2 = st.columns(2)

			with col1:
				if st.button(f"Remove duplicates from the file: {file.name}"):
					df.drop_duplicates(inplace=True)
					st.success(" ☑️ Duplicates removed successfully!")

	 with col2:
				if st.button(f"Remove missing values from the file: {file.name}"):
					numeric_cols = df.select_dtypes(include=["number"]).columns
					df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
					st.success(" ☑️ Missing values filled successfully!")
					
		# data visualization 
