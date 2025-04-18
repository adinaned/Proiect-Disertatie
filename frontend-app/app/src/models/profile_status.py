from sqlalchemy import Column, Integer, Date, Enum
from src.db.database import Base
from enum import Enum as PyEnum


class ProfileStatusEnum(PyEnum):
    ACTIVE = "active"
    OPEN = "open"
    SUSPENDED = "suspended"
    CLOSED = "closed"


class ProfileStatus(Base):
    __tablename__ = "profile_statuses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(ProfileStatusEnum), index=True, default=ProfileStatusEnum.OPEN)
    updated_at = Column(Date, index=True)
