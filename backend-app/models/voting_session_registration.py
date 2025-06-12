from sqlalchemy import Column, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from . import db


class VotingSessionRegistration(db.Model):
    __tablename__ = "voting_session_registrations"

    voting_session_id = Column(CHAR(36), ForeignKey("voting_sessions.id"), nullable=False)
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)

    voting_session = relationship("VotingSession", back_populates="registrations")
    user = relationship("User", back_populates="registrations")

    __table_args__ = (
        PrimaryKeyConstraint("voting_session_id", "user_id"),
    )

    def to_dict(self):
        return {
            "voting_session_id": self.voting_session_id,
            "user_id": self.user_id,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
