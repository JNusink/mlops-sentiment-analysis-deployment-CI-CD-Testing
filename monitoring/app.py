import streamlit as st
import os
import pandas as pd

# Set log directory (project-relative, not /app)
current_dir = os.path.dirname(__file__)
log_dir = os.path.join(current_dir, "..", "logs")
os.makedirs(log_dir, exist_ok=True)

# Read log file
log_file = os.path.join(log_dir, "sentiment.log")
if os.path.exists(log_file):
    df = pd.read_csv(log_file)
else:
    df = pd.DataFrame(columns=["timestamp", "text", "sentiment", "confidence"])

st.title("Sentiment Analysis Dashboard")
st.write("Recent Predictions (Last 10):")

if not df.empty:
    st.table(df.tail(10))
else:
    st.write("No logs available yet.")
