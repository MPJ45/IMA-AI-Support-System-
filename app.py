import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import matplotlib.pyplot as plt

st.set_page_config(page_title="IMA I20 AI Support System", layout="wide")

# Define the scopes explicitly
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from Streamlit secrets and create authorized client
try:
    creds_dict = st.secrets["google_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
except Exception as e:
    st.error(f"Failed to load Google credentials: {e}")
    st.stop()

# Open Google Sheet by URL once
try:
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1GjfnGfWaE6dDtNU9fCjK9SRz8MWXlxTNaYip0Fctu70"
    sheet = gc.open_by_url(SHEET_URL)
    worksheet = sheet.sheet1
except Exception as e:
    st.error(f"Failed to open Google Sheet: {e}")
    st.stop()

# Load data function with error handling
def load_data():
    try:
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data from sheet: {e}")
        return pd.DataFrame()

# Append a row
def append_data(row):
    try:
        worksheet.append_row(row)
    except Exception as e:
        st.error(f"Error appending data: {e}")

# Update entire sheet
def update_sheet(df):
    try:
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Error updating sheet: {e}")

df = load_data()

# The rest of your Streamlit UI code below...

st.title("📊 IMA I20 AI Support System")
st.markdown("Track machine performance, log issues, and get predictive insights.")

# Your existing UI code for logging entries, charts, and editing follows here...
