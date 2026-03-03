import streamlit as st
import requests

# =====================================
# PAGE CONFIG (MUST BE FIRST)
# =====================================
st.set_page_config(page_title="Skoolnect Sage", layout="centered")

st.title("🧠 Skoolnect Sage")

# =====================================
# SESSION STATE INITIALIZATION
# =====================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "role" not in st.session_state:
    st.session_state.role = "teacher"


# =====================================
# SIDEBAR
# =====================================
with st.sidebar:

    st.header("💬 Conversations")

    # New Chat Button
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.session_state.conversation_id = None

    st.divider()

    # Fetch conversations from backend
    try:
        res = requests.get("http://127.0.0.1:8000/conversations")
        conversations = res.json()
    except:
        conversations = []

    for conv in conversations:
        if st.button(f"Chat {conv['id']}"):
            st.session_state.conversation_id = conv["id"]

            # Load messages for that conversation
            try:
                res = requests.get(
                    f"http://127.0.0.1:8000/conversations/{conv['id']}"
                )
                old_messages = res.json()

                st.session_state.messages = [
                    {
                        "role": msg["role"],
                        "content": msg["content"]
                    }
                    for msg in old_messages
                ]
            except:
                st.session_state.messages = []


# =====================================
# ROLE SELECTOR (PER SESSION)
# =====================================
st.session_state.role = st.selectbox(
    "Role",
    ["teacher", "parent"],
    index=0 if st.session_state.role == "teacher" else 1
)


# =====================================
# DISPLAY CHAT HISTORY
# =====================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# =====================================
# CHAT INPUT
# =====================================
if prompt := st.chat_input("Ask Skoolnect Sage something..."):

    # Display user message immediately
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    try:
        with st.chat_message("assistant"):
            with st.spinner("Sage is thinking..."):

                res = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "role": st.session_state.role,
                        "message": prompt,
                        "conversation_id": st.session_state.conversation_id
                    }
                )

                data = res.json()
                assistant_reply = data.get("response", "An error occurred.")

                # Update conversation ID if new
                if "conversation_id" in data:
                    st.session_state.conversation_id = data["conversation_id"]

    except Exception as e:
        assistant_reply = f"Frontend Error: {str(e)}"

    # Save assistant reply
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_reply)