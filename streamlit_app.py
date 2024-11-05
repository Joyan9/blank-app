import gspread
from google.oauth2.service_account import Credentials
import time
import streamlit as st
import os
import json

# Define the Google Sheets API scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Convert the AttrDict to a regular dictionary
service_account_info = dict(st.secrets["gcp_service_account"])

# Write the service account info to a temporary JSON file
with open("service_account_key.json", "w") as f:
    json.dump(service_account_info, f)

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"

# Authenticate using the credentials from the environment variable
creds = Credentials.from_service_account_file(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], scopes=scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name or URL
sheet = client.open('IU Unit Test Generator Logs').worksheet('Logs')  

def log_metrics(time_taken, tokens_used):
    # Add the metrics to the next available row in Google Sheets
    sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), time_taken, tokens_used])

# Example usage in Streamlit
if st.button("Run Task"):
    start_time = time.time()
    
    # ... (Run your app's main processing logic here) ...
    
    # Example metrics (replace with actual values)
    time_taken = round(time.time() - start_time, 2)  # Measure the time taken
    tokens_used = st.session_state.get("tokens_used", 20)  # Fetch tokens used from session state
    
    # Log metrics to Google Sheets
    log_metrics(time_taken, tokens_used)
    st.write("Metrics logged to Google Sheets.")
