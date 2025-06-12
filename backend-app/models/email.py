from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db


class Email(db.Model):
    __tablename__ = "emails"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    email_address = Column(String(320), index=True, nullable=False)
    is_verified = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="email")

    def to_dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "email_address": self.email_address,
                "is_verified": self.is_verified,
                "created_at": self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()