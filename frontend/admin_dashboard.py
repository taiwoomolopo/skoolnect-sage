import streamlit as st
import requests

st.set_page_config(page_title="Skoolnect Admin", layout="wide")
st.title("📊 Skoolnect Admin Dashboard")

BASE_URL = "https://skoolnect-backend.onrender.com"

# ===============================
# CONVERSATIONS OVERVIEW
# ===============================
st.header("All Conversations")

try:
    res = requests.get(f"{BASE_URL}/conversations")
    conversations = res.json() if res.status_code == 200 else []
except:
    conversations = []

st.metric("Total Conversations", len(conversations))

st.divider()

# ===============================
# VIEW CONVERSATION DETAILS
# ===============================
selected_conv = st.selectbox(
    "Select Conversation ID",
    [conv["id"] for conv in conversations] if conversations else []
)

if selected_conv:
    try:
        res = requests.get(f"{BASE_URL}/conversations/{selected_conv}")
        messages = res.json() if res.status_code == 200 else []
    except:
        messages = []

    st.subheader(f"Conversation {selected_conv}")

    for msg in messages:
        st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")
        st.divider()