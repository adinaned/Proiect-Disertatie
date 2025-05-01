from sqlalchemy import Column, Integer, String, ForeignKey
from src.db.database import Base

class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    session_id = Column(Integer, ForeignKey("voting_sessions.id"))