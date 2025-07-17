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

# Upload reference file
reference_file = st.file_uploader("📁 Upload the reference file (Excel or CSV):", type=["xlsx", "csv"])

# Upload comparison files
comparison_files = st.file_uploader("📂 Upload one or more files to compare (Excel or CSV):", type=["xlsx", "csv"], accept_multiple_files=True)

# Function to load files with fallback CSV separators
def load_file(file):
    try:
        if file.name.endswith('.csv'):
            try:
                return pd.read_csv(file, on_bad_lines='skip', sep=';')
            except:
                file.seek(0)
                return pd.read_csv(file, on_bad_lines='skip', sep=',')
        elif file.name.endswith('.xlsx'):
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"❌ Error loading file {file.name}: {e}")
    return pd.DataFrame()

# Safe DataFrame display (convert to string to avoid ArrowTypeError)
def show_df_safely(df, title=None):
    if title:
        st.subheader(title)
    try:
        st.dataframe(df.astype(str))
    except:
        st.warning("⚠️ Could not display DataFrame due to data type issues.")

if reference_file and comparison_files:
    ref_df = load_file(reference_file)
    if 'Name' not in ref_df.columns:
        st.error("❌ 'Name' column not found in the reference file.")
    else:
        reference_names = ref_df['Name'].dropna().astype(str).str.strip().unique()
        all_duplicates = []

        st.markdown(f"ℹ️ Reference file: **{reference_file.name}** will not be modified.")

        for uploaded_file in comparison_files:
            comp_df = load_file(uploaded_file)
            if 'Name' in comp_df.columns:
                comparison_names = comp_df['Name'].dropna().astype(str).str.strip()
                duplicates = comparison_names[comparison_names.isin(reference_names)].unique()

                if len(duplicates) > 0:
                    result_df = pd.DataFrame({'Duplicate Name': duplicates})
                    result_df['Source File'] = uploaded_file.name
                    all_duplicates.append(result_df)

                    show_df_safely(result_df, f"🔍 Duplicates in: {uploaded_file.name}")

                    # Download duplicates
                    output = BytesIO()
                    result_df.to_excel(output, index=False, engine='openpyxl')
                    output.seek(0)
                    st.download_button(
                        label=f"📥 Download Duplicates from {uploaded_file.name}",
                        data=output,
                        file_name=f"duplicates_in_{uploaded_file.name.replace('.xlsx', '').replace('.csv', '')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                    # Option to remove duplicates from this comparison file
                    if st.checkbox(f"🧹 Remove duplicates from {uploaded_file.name}?"):
                        comp_df['Name_stripped'] = comp_df['Name'].astype(str).str.strip()
                        cleaned_df = comp_df[~comp_df['Name_stripped'].isin(duplicates)].drop(columns=['Name_stripped'])

                        st.success(f"{len(comp_df) - len(cleaned_df)} duplicate entries removed from {uploaded_file.name}.")
                        show_df_safely(cleaned_df, f"🧾 Cleaned: {uploaded_file.name}")

                        cleaned_output = BytesIO()
                        cleaned_df.to_excel(cleaned_output, index=False, engine='openpyxl')
                        cleaned_output.seek(0)
                        st.download_button(
                            label=f"📥 Download cleaned {uploaded_file.name}",
                            data=cleaned_output,
                            file_name=f"cleaned_{uploaded_file.name.replace('.xlsx', '').replace('.csv', '')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.info(f"✅ No duplicates found in: {uploaded_file.name}")
            else:
                st.warning(f"⚠️ 'Name' column not found in file: {uploaded_file.name}")
else:
    st.warning("⚠️ Please upload both the reference file and at least one comparison file.")
