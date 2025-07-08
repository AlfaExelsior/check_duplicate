
# 🚀 Exelsior Duplicate Checker

**Futuristic Streamlit app** to detect duplicate names between a reference Excel/CSV file and multiple comparison files.

## ✨ Features

- Upload one reference file (Excel or CSV)
- Upload multiple comparison files (Excel or CSV)
- Automatically detects duplicates in the `Name` column
- Stylish futuristic UI
- Download the results as an Excel file

## 📁 Supported File Formats

- `.xlsx`
- `.csv`

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/AlfaExelsior/exelsior-duplicate-checker.git
cd exelsior-duplicate-checker
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install required packages:

```bash
pip install -r requirements.txt
```

## 🚦 How to Run

```bash
streamlit run app.py
```

This will open the app in your web browser.

## 📥 Output

- If duplicates are found, they will be listed in the app and available for download as an Excel file.
- If no duplicates are found, you’ll see a confirmation message.

---

👤 Created by [AlfaExelsior](https://github.com/AlfaExelsior)
