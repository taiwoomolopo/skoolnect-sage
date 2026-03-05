import streamlit as st
import requests

st.set_page_config(page_title="Skoolnect Sage", layout="wide")

BASE_URL = "https://skoolnect-backend.onrender.com"

st.title("🧠 Skoolnect Sage")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

# SIDEBAR
with st.sidebar:

    st.header("Conversations")

    if st.button("New Chat"):
        st.session_state.messages = []
        st.session_state.conversation_id = None

    try:
        res = requests.get(f"{BASE_URL}/conversations")
        conversations = res.json()
    except:
        conversations = []

    for conv in conversations:

        title = conv.get("title", f"Chat {conv['id']}")

        if st.button(title):

            st.session_state.conversation_id = conv["id"]

        res = requests.get(
            f"{BASE_URL}/conversations/{conv['id']}"
        )

        st.session_state.messages = res.json()

# CHAT DISPLAY
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Ask Skoolnect Sage...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    res = requests.post(
        f"{BASE_URL}/chat",
        json={
            "role": "teacher",
            "message": prompt,
            "conversation_id": st.session_state.conversation_id
        }
    )

    data = res.json()

    reply = data["response"]

    st.session_state.conversation_id = data["conversation_id"]

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.markdown(reply)