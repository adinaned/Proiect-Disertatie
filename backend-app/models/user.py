from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import CHAR
import uuid

from . import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="RESTRICT"), nullable=False, index=True)
    city = Column(String(100), nullable=False)
    address = Column(String(256), nullable=False)
    national_id = Column(Integer, nullable=False, unique=True)
    organization_id = Column(CHAR(36), ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=False, index=True)
    role_id = Column(CHAR(36), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=True, index=True)
    created_at = Column(DateTime, nullable=False)

    country = relationship("Country", back_populates="users")
    email = relationship("Email", back_populates="user", cascade="all, delete-orphan")
    organization = relationship("Organization", back_populates="users")
    password = relationship("Password", back_populates="user", cascade="all, delete-orphan")
    profile_status = relationship("ProfileStatus", back_populates="user", cascade="all, delete-orphan")
    registrations = relationship("VotingSessionRegistration", back_populates="user")
    role = relationship("Role", back_populates="users")

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "date_of_birth": self.date_of_birth,
                "address": self.address,
                "country_id": self.country_id,
                "city": self.city,
                "national_id": self.national_id,
                "organization_id": self.organization_id,
                "role_id": self.role_id,
                "created_at": self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()
