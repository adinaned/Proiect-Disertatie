from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

import uuid

from . import db

class Option(db.Model):
    __tablename__ = "options"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), index=True)
    voting_session_id = Column(CHAR(36), ForeignKey("voting_sessions.id"))

    voting_session = relationship("VotingSession", back_populates="options")
    votes = relationship("Vote", back_populates="option", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "voting_session_id": self.voting_session_id
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
