import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from app.core.config import settings

st.set_page_config(page_title="Skoolnect Sage Admin", layout="wide")

st.title("🧠 Skoolnect Sage — Admin Dashboard")

# Connect to DB
engine = create_engine(settings.DATABASE_URL)

# Sidebar navigation
section = st.sidebar.selectbox(
    "Select Section",
    ["Overview", "Users", "Conversations", "Usage Monitoring"]
)

if section == "Overview":
    st.header("System Overview")

    users_count = pd.read_sql("SELECT COUNT(*) as count FROM users", engine)
    conv_count = pd.read_sql("SELECT COUNT(*) as count FROM conversations", engine)
    usage_total = pd.read_sql("SELECT SUM(tokens_used) as total FROM usage", engine)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Users", users_count["count"][0] if not users_count.empty else 0)
    col2.metric("Total Conversations", conv_count["count"][0] if not conv_count.empty else 0)
    col3.metric("Total Tokens Used", usage_total["total"][0] if not usage_total.empty else 0)
    
if section == "Users":
    st.header("Users")

    users_df = pd.read_sql("SELECT * FROM users", engine)
    st.dataframe(users_df)
    
    
if section == "Conversations":
    st.header("Conversations")

    conv_df = pd.read_sql("SELECT * FROM conversations", engine)
    st.dataframe(conv_df)
    
    
if section == "Usage Monitoring":
    st.header("Token Usage")

    usage_df = pd.read_sql("SELECT * FROM usage", engine)
    st.dataframe(usage_df)

    if not usage_df.empty:
        st.subheader("Token Usage Over Time")
        usage_df["timestamp"] = pd.to_datetime(usage_df["timestamp"])
        chart_data = usage_df.groupby(usage_df["timestamp"].dt.date)["tokens_used"].sum()
        st.line_chart(chart_data)
        
        
