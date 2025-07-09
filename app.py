
import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Exelsior Duplicate Checker", layout="centered")

# 💫 Custom Futuristic Styling
st.markdown("""
    <style>
        body {background-color: #0f2027; color: white;}
        .stButton button {
            background-color: #00ffd9;
            color: black;
            font-weight: bold;
            border-radius: 10px;
        }
        .stFileUploader {border: 2px solid #00ffd9; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Exelsior Duplicate Checker")

st.write("Upload your main Excel or CSV file and one or more files (CSV or Excel) to check for duplicates based on the 'Name' column.")

# Upload reference file (Excel or CSV)
reference_file = st.file_uploader("📁 Upload the reference file (Excel or CSV):", type=["xlsx", "csv"])

# Upload one or more files to compare
comparison_files = st.file_uploader("📂 Upload one or more files to compare (Excel or CSV):", type=["xlsx", "csv"], accept_multiple_files=True)

def load_file(file):
    try:
        if file.name.endswith('.csv'):
            return pd.read_csv(file, on_bad_lines='skip', sep=';')  # Handles semicolon-separated CSVs
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"❌ Error loading file {file.name}: {e}")
    return pd.DataFrame()  # Return empty if loading fails

if reference_file and comparison_files:
    ref_df = load_file(reference_file)
    if 'Name' not in ref_df.columns:
        st.error("❌ 'Name' column not found in the reference file.")
    else:
        reference_names = ref_df['Name'].dropna().astype(str).str.strip().unique()
        all_duplicates = []

        for uploaded_file in comparison_files:
            comp_df = load_file(uploaded_file)
            if 'Name' in comp_df.columns:
                comparison_names = comp_df['Name'].dropna().astype(str).str.strip()
                duplicates = comparison_names[comparison_names.isin(reference_names)].unique()
                result_df = pd.DataFrame({'Duplicate Name': duplicates})
                result_df['Source File'] = uploaded_file.name
                all_duplicates.append(result_df)
            else:
                st.warning(f"⚠️ 'Name' column not found in file: {uploaded_file.name}")

        if all_duplicates:
            final_result = pd.concat(all_duplicates, ignore_index=True)

            st.subheader("🔍 Duplicates Found")
            st.dataframe(final_result)

            # Prepare file for download
            output = BytesIO()
            final_result.to_excel(output, index=False, engine='openpyxl')
            output.seek(0)

            st.download_button(
                label="📥 Download Results as Excel",
                data=output,
                file_name="duplicate_names_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("✅ No duplicates found in the uploaded files.")
else:
    st.warning("⚠️ Please upload both the reference file and at least one comparison file.")
