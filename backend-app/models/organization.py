from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db


class Organization(db.Model):
    __tablename__ = "organizations"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String(100), unique=True, nullable=False, index=True)

    roles = relationship("Role", back_populates="organization", cascade="all, delete-orphan", passive_deletes=True)
    users = relationship("User", back_populates="organization")
    voting_sessions = relationship("VotingSession", back_populates="organization")

    def to_dict(self):
        return {"id": self.id,
                "name": self.name, }

    def save(self):
        db.session.add(self)
        db.session.commit()
