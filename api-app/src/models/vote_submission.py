from sqlalchemy import Column, Integer, Boolean, ForeignKey
from src.db.database import Base

class VoteSubmission(Base):
    __tablename__ = "vote_submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"), index=True)
    has_voted = Column(Boolean, default=False)
