from enum import Enum as PyEnum
from sqlalchemy import Column, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
import uuid

from sqlalchemy.orm import relationship

from . import db


class ProfileStatusEnum(PyEnum):
    ACTIVE = "active"
    PENDING = "pending"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class ProfileStatus(db.Model):
    __tablename__ = "profile_statuses"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(CHAR(36), ForeignKey("users.id"), nullable=False, index=True)
    name = Column(Enum(ProfileStatusEnum), index=True, default=ProfileStatusEnum.PENDING)
    updated_at = Column(DateTime)

    user = relationship("User", back_populates="profile_status")

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name,
                "updated_at": self.updated_at}

    def save(self):
        db.session.add(self)
        db.session.commit()

