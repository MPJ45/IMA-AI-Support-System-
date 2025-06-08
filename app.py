import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt

st.set_page_config(page_title="IMA I20 AI Support System", layout="wide")

# Google Sheets Setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
from google.oauth2.service_account import Credentials
import gspread
import streamlit as st

# Load credentials from Streamlit Secrets
creds_dict = st.secrets["google_service_account"]
creds = Credentials.from_service_account_info(creds_dict)

# Authorize with gspread
gc = gspread.authorize(creds)

# Open your sheet by URL
sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GjfnGfWaE6dDtNU9fCjK9SRz8MWXlxTNaYip0Fctu70")
worksheet = sheet.sheet1

CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open_by_url("https://docs.google.com/spreadsheets/d/1GjfnGfWaE6dDtNU9fCjK9SRz8MWXlxTNaYip0Fctu70")
worksheet = SHEET.sheet1

# Load data
def load_data():
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

# Save new row
def append_data(row):
    worksheet.append_row(row)

# Editable table (updating entire sheet)
def update_sheet(df):
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

df = load_data()

st.title("📊 IMA I20 AI Support System")
st.markdown("Track machine performance, log issues, and get predictive insights.")

# Section 1: Log new entry
with st.expander("➕ Log New Shift Entry", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        operator_id = st.text_input("Operator ID (e.g. PNG1080)", max_chars=12)
        machine = st.selectbox("Select Machine", [
            "Press 40", "Wrapper 41", "Press 42", "Wrapper 43", "Press 44", "Wrapper 45", "Press 46", "Wrapper 47",
            "Press 48", "Wrapper 49", "Press 50", "Wrapper 51", "Press 62", "Wrapper 63", "Press 64", "Wrapper 65",
            "Press 66", "Wrapper 67", "Press 68", "Wrapper 69", "Press 80", "Wrapper 81", "Press 82", "Wrapper 83",
            "Press 84", "Wrapper 85", "Press 86", "Wrapper 87", "Press 88", "Wrapper 89"
        ])
        oee = st.number_input("OEE (%)", min_value=0.0, max_value=100.0, step=0.1)
        runtime = st.number_input("Runtime (minutes)", min_value=0)
        downtime = st.number_input("Downtime (minutes)", min_value=0)

    with col2:
        date = st.date_input("Date")
        shift = st.selectbox("Shift", ["DAY A", "NIGHT A", "DAY B", "NIGHT B"])
        issue = st.text_area("Issue Encountered")
        fix = st.text_area("Fix / Action Taken")

    if st.button("Submit Entry"):
        row = [date.strftime("%Y-%m-%d"), shift, machine, oee, runtime, downtime, issue, fix, operator_id]
        append_data(row)
        st.success("Entry logged successfully.")
        df = load_data()

# Section 2: Charts and filters
st.markdown("## 📈 Performance Charts")
machines = df['Machine'].unique().tolist()
selected_machines = st.multiselect("Select Machines to View", machines, default=machines)

filtered_df = df[df['Machine'].isin(selected_machines)]

if not filtered_df.empty:
    fig, axes = plt.subplots(1, 3, figsize=(18, 4))
    filtered_df.groupby("Machine")["OEE (%)"].mean().plot(kind="bar", ax=axes[0], title="Average OEE")
    filtered_df.groupby("Machine")["Runtime (minutes)"].sum().plot(kind="bar", ax=axes[1], title="Total Runtime")
    filtered_df.groupby("Machine")["Downtime (minutes)"].sum().plot(kind="bar", ax=axes[2], title="Total Downtime")
    st.pyplot(fig)
else:
    st.info("No data to display for selected machines.")

# Section 3: Full log view + editing
st.markdown("## 🧾 Log History and Edits")
edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")

if st.button("💾 Save Changes to Log"):
    update_sheet(edited_df)
    st.success("Changes saved successfully.")

st.markdown("---")
st.caption("📌 Built for IMA I20 Maintenance - Powered by AI 🔧")
