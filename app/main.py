# app/main.py

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.services.llm_service import generate_response
from app.services.rag_service import retrieve_context
from app.services.memory_service import (
    create_conversation,
    save_message,
    get_all_conversations,
    get_conversation_messages
)
from app.services.usage_service import save_usage, get_usage_stats
from app.prompts.master_prompt import MASTER_PROMPT
from app.prompts.teacher_mode import TEACHER_MODE
from app.prompts.parent_mode import PARENT_MODE

app = FastAPI()

# -------------------------------
# CORS MIDDLEWARE
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "https://skoolnect-sage-userui.onrender.com",
        "https://skoolnect-sage-admin.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# REQUEST MODEL
# -------------------------------
class ChatRequest(BaseModel):
    role: str
    message: str
    conversation_id: int | None = None

# -------------------------------
# CHAT ENDPOINT
# -------------------------------
@app.post("/chat")
def chat(request: ChatRequest):

    mode_prompt = TEACHER_MODE if request.role == "teacher" else PARENT_MODE
    context = retrieve_context(request.message)

    messages = [
        {"role": "system", "content": MASTER_PROMPT},
        {"role": "system", "content": mode_prompt},
        {"role": "system", "content": f"Knowledge:\n{context}"},
        {"role": "user", "content": request.message}
    ]

    response, tokens = generate_response(messages)

    # create conversation if new
    if not request.conversation_id:
        title = request.message[:40]
        conversation_id = create_conversation(request.role, title)
    else:
        conversation_id = request.conversation_id

    save_message(conversation_id, "user", request.message)
    save_message(conversation_id, "assistant", response)

    save_usage(user_id=1, tokens=tokens)

    return {
        "response": response,
        "conversation_id": conversation_id
    }

# -------------------------------
# GET CONVERSATIONS
# -------------------------------
@app.get("/conversations")
def list_conversations():
    conversations = get_all_conversations()
    return conversations

# -------------------------------
# GET MESSAGES
# -------------------------------
@app.get("/conversations/{conversation_id}")
def conversation_messages(conversation_id: int):
    return get_conversation_messages(conversation_id)

# -------------------------------
# USAGE STATS
# -------------------------------
@app.get("/usage")
def usage():
    return get_usage_stats()