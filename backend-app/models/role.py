from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db


class Role(db.Model):
    __tablename__ = "roles"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    organization_id = Column(CHAR(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)

    organization = relationship("Organization", back_populates="roles")
    users = relationship("User", back_populates="role")
    voting_sessions = relationship("VotingSession", back_populates="role")

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "organization_id": self.organization_id}

    def save(self):
        db.session.add(self)
        db.session.commit()
