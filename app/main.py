from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from app.db.init_db import init_db

from app.prompts.master_prompt import MASTER_PROMPT
from app.prompts.teacher_mode import TEACHER_MODE
from app.prompts.parent_mode import PARENT_MODE
from app.services.llm_service import generate_response
from app.services.rag_service import retrieve_context
from app.services.memory_service import (
    create_conversation,
    save_message,
    get_all_conversations,
    get_messages
)
from app.utils.logging import logger


app = FastAPI()


# ==============================
# REQUEST MODELS
# ==============================

class ChatRequest(BaseModel):
    role: str
    message: str
    conversation_id: Optional[int] = None


# ==============================
# LIST ALL CONVERSATIONS
# ==============================

@app.get("/conversations")
def list_conversations():
    conversations = get_all_conversations()

    return [
        {
            "id": conv.id,
            "role": conv.role,
            "created_at": conv.created_at
        }
        for conv in conversations
    ]


# ==============================
# LOAD SINGLE CONVERSATION MESSAGES
# ==============================

@app.get("/conversations/{conversation_id}")
def load_conversation(conversation_id: int):
    messages = get_messages(conversation_id)

    return [
        {
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]


# ==============================
# CHAT ENDPOINT
# ==============================

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        logger.info("Chat request received")

        # Determine conversation
        if request.conversation_id:
            conversation_id = request.conversation_id
        else:
            conversation_id = create_conversation(request.role)

        # Select role prompt
        mode_prompt = (
            TEACHER_MODE if request.role == "teacher"
            else PARENT_MODE
        )

        # Retrieve RAG context
        context = retrieve_context(request.message)

        # Build messages for LLM
        messages = [
            {"role": "system", "content": MASTER_PROMPT},
            {"role": "system", "content": mode_prompt},
            {"role": "system", "content": f"Relevant Skoolnect Knowledge:\n{context}"},
            {"role": "user", "content": request.message}
        ]

        # Generate AI response
        response = generate_response(messages)

        # Persist messages
        save_message(conversation_id, "user", request.message)
        save_message(conversation_id, "assistant", response)

        return {
            "response": response,
            "conversation_id": conversation_id
        }

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return {
            "response": "An error occurred. Please check logs."
        }
        
 # ==============================
# HEALTH CHECK
# ==============================       

@app.get("/")
def health():
    return {"status": "ok"}
    
    
@app.on_event("startup")
def startup():
    init_db()    