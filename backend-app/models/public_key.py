from sqlalchemy import Column, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

import uuid
from . import db


class PublicKey(db.Model):
    __tablename__ = 'public_keys'

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    voting_session_id = Column(CHAR(36), ForeignKey("voting_sessions.id"), nullable=False)
    public_key_x = Column(String(100), nullable=False)
    public_key_y = Column(String(100), nullable=False)

    voting_session = relationship("VotingSession", back_populates="public_keys")

    def to_dict(self):
        return {"id": self.id,
                "voting_session_id": self.voting_session_id,
                "public_key_x": self.public_key_x,
                "public_key_y": self.public_key_y}

    def save(self):
        db.session.add(self)
        db.session.commit()
