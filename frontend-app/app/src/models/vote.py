from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.db.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    token = Column(String(256))
    submission_timestamp = Column(Date)
