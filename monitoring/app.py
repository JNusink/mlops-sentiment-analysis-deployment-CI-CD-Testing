import os
import streamlit as st
import json

st.title("Sentiment Analysis Monitoring Dashboard")

log_dir = "/app/logs"  # Match the volume mount path
log_file = os.path.join(log_dir, "sentiment.log")

if os.path.exists(log_file):
    with open(log_file, "r") as f:
        logs = [json.loads(line.strip()) for line in f.readlines() if line.strip()]
    st.write("Recent Predictions (Last 10):")
    for log in logs[-10:]:
        st.write(f"Sentiment: {log['sentiment']}, Confidence: {log['confidence']:.2f}")
else:
    st.write("No logs available yet. Make a prediction via the API.")