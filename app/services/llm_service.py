from openai import OpenAI
from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import Usage


client = OpenAI(api_key=settings.OPENAI_API_KEY)


    
    
def generate_response(messages, user_id=None):
    response = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=messages
    )

    tokens_used = response.usage.total_tokens

    # Save usage to database
    db = SessionLocal()
    usage_entry = Usage(
        user_id=user_id,
        tokens_used=tokens_used
    )
    db.add(usage_entry)
    db.commit()
    db.close()

    return response.choices[0].message.content