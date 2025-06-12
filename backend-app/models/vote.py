from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import JSON, CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db


class Vote(db.Model):
    __tablename__ = "votes"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    voting_session_id = Column(CHAR(36), ForeignKey("voting_sessions.id"))
    option_id = Column(CHAR(36), ForeignKey("options.id"))
    token = Column(String(256),  nullable=False)
    key_image = Column(String(256), nullable=False)
    ring_hash = Column(String(256), nullable=False)
    signature = Column(JSON, nullable=False)
    submission_timestamp = Column(DateTime, nullable=False)

    voting_session = relationship("VotingSession", back_populates="votes")
    option = relationship("Option", back_populates="votes")

    def to_dict(self):
        return {
            "id": self.id,
            "voting_session_id": self.voting_session_id,
            "option_id": self.option_id,
            "token": self.token,
            "key_image": self.key_image,
            "ring_hash": self.ring_hash,
            "signature": self.signature,
            "submission_timestamp": self.submission_timestamp
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
