from app.db.session import SessionLocal
from app.models.usage import Usage

def save_usage(user_id: int, tokens: int):

    db = SessionLocal()

    usage = Usage(
        user_id=user_id,
        tokens_used=tokens
    )

    db.add(usage)
    db.commit()
    db.close()

def get_usage_stats():

    db = SessionLocal()

    data = db.query(Usage).all()

    db.close()

    return [
        {
            "user_id": u.user_id,
            "tokens_used": u.tokens_used,
            "timestamp": u.timestamp
        }
        for u in data
    ]