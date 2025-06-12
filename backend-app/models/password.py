from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db

class Password(db.Model):
    __tablename__ = "passwords"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False)
    password = Column(String(128), nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="password")

    def to_dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "password": self.password,
                "updated_at": self.updated_at}

    def save(self):
        db.session.add(self)
        db.session.commit()