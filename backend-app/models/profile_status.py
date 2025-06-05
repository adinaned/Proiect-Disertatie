from sqlalchemy import Column, Integer, Date, Enum
from . import db
from enum import Enum as PyEnum


class ProfileStatusEnum(PyEnum):
    ACTIVE = "active"
    OPEN = "open"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class ProfileStatus(db.Model):
    __tablename__ = "profile_statuses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    name = Column(Enum(ProfileStatusEnum), index=True, default=ProfileStatusEnum.OPEN)
    updated_at = Column(Date, index=True)

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name,
                "updated_at": self.updated_at}

    def save(self):
        db.session.add(self)
        db.session.commit()

