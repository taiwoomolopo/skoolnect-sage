import streamlit as st
import requests

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="Skoolnect Sage", layout="centered")
st.title("🧠 Skoolnect Sage")

BASE_URL = "https://skoolnect-backend.onrender.com"

# ===============================
# SESSION STATE
# ===============================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "role" not in st.session_state:
    st.session_state.role = "teacher"

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.header("💬 Conversations")

    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.conversation_id = None

    st.divider()

    # Fetch conversations
    try:
        res = requests.get(f"{BASE_URL}/conversations")
        conversations = res.json() if res.status_code == 200 else []
    except:
        conversations = []

    for conv in conversations:
        if st.button(f"Chat {conv['id']}"):
            st.session_state.conversation_id = conv["id"]

            try:
                res = requests.get(
                    f"{BASE_URL}/conversations/{conv['id']}"
                )
                old_messages = res.json() if res.status_code == 200 else []

                st.session_state.messages = [
                    {
                        "role": msg["role"],
                        "content": msg["content"]
                    }
                    for msg in old_messages
                ]
            except:
                st.session_state.messages = []

# ===============================
# ROLE SELECTOR
# ===============================
st.session_state.role = st.selectbox(
    "Role",
    ["teacher", "parent"],
    index=0 if st.session_state.role == "teacher" else 1
)

# ===============================
# DISPLAY CHAT
# ===============================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===============================
# CHAT INPUT
# ===============================
if prompt := st.chat_input("Ask Skoolnect Sage something..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):

                res = requests.post(
                    f"{BASE_URL}/chat",
                    json={
                        "role": st.session_state.role,
                        "message": prompt,
                        "conversation_id": st.session_state.conversation_id
                    }
                )

                if res.status_code == 200:
                    data = res.json()
                    assistant_reply = data.get("response", "Error.")

                    if "conversation_id" in data:
                        st.session_state.conversation_id = data["conversation_id"]
                else:
                    assistant_reply = "Backend error."

    except Exception as e:
        assistant_reply = f"Frontend error: {str(e)}"

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)