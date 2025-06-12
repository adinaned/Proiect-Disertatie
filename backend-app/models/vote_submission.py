from sqlalchemy import Column, Integer, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import CHAR
import uuid

from sqlalchemy.orm import relationship
from . import db


class VoteSubmission(db.Model):
    __tablename__ = "vote_submissions"

    id = Column(CHAR(36), default=lambda: str(uuid.uuid4()))
    voting_session_id = Column(CHAR(36), ForeignKey("voting_sessions.id"), index=True, nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.id"), index=True, nullable=False)

    voting_session = relationship("VotingSession", back_populates="vote_submissions")

    # user = relationship("User", back_populates="vote_submissions")
    __table_args__ = (
        PrimaryKeyConstraint("voting_session_id", "user_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "voting_session_id": self.voting_session_id,
            "user_id": self.user_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
