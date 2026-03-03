from app.db.session import SessionLocal
from app.db.models import Conversation, Message

def create_conversation(role):
    db = SessionLocal()
    conv = Conversation(role=role)
    db.add(conv)
    db.commit()
    db.refresh(conv)
    db.close()
    return conv.id

def save_message(conversation_id, role, content):
    db = SessionLocal()
    msg = Message(conversation_id=conversation_id, role=role, content=content)
    db.add(msg)
    db.commit()
    db.close()
    
    
def get_messages(conversation_id):
    db = SessionLocal()
    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).all()
    db.close()
    return messages

def get_all_conversations():
    db = SessionLocal()
    conversations = db.query(Conversation).order_by(
        Conversation.created_at.desc()
    ).all()
    db.close()
    return conversations    
    
def delete_conversation(conversation_id):
    db = SessionLocal()
    db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).delete()
    db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).delete()
    db.commit()
    db.close()    
    
    
def get_conversation_messages(conversation_id):
    db = SessionLocal()
    messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
    db.close()
    return [{"role": m.role, "content": m.content} for m in messages]    