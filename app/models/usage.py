from sqlalchemy import Column, Integer, DateTime
from datetime import datetime
from app.db.base import Base

class Usage(Base):

    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    tokens_used = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)