from sqlalchemy import Column, Integer, String, ForeignKey
from src.db.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    voting_session_id = Column(Integer, ForeignKey("voting_sessions.id"), index=True)
