import streamlit as st
import requests

BASE_URL = "https://skoolnect-backend.onrender.com"

ADMIN_PASSWORD = "admin123"

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:

    pwd = st.text_input("Admin Password", type="password")

    if st.button("Login"):

        if pwd == ADMIN_PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong password")

    st.stop()

st.title("Skoolnect Admin Dashboard")

# ---------------------
# USAGE MONITORING
# ---------------------

st.header("Usage Monitoring")

try:
    res = requests.get(f"{BASE_URL}/usage")
    data = res.json()

 # Ensure backend returned a list
    if isinstance(data, list):
        usage = data

        total_tokens = sum(u["tokens_used"] for u in usage)

        st.metric("Total Tokens Used", total_tokens)

        st.subheader("Usage Records")
        st.json(usage)

    else:

        st.error("Unexpected response from backend")
        st.json(data)

except Exception as e:
    st.error(f"Error fetching usage: {str(e)}")



# ---------------------
# CONVERSATIONS
# ---------------------

st.header("Conversations")

res = requests.get(f"{BASE_URL}/conversations")
conversations = res.json()

selected = st.selectbox(
    "Select conversation",
    [c["id"] for c in conversations]
)

if selected:

    res = requests.get(
        f"{BASE_URL}/conversations/{selected}"
    )

    messages = res.json()

    for m in messages:

        st.write(f"**{m['role']}**")
        st.write(m["content"])
        st.divider()