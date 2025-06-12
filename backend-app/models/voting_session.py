from sqlalchemy import Column, String, DateTime, ForeignKey, null
from sqlalchemy.dialects.mysql import JSON, CHAR
from sqlalchemy.orm import relationship
import uuid

from . import db


class VotingSession(db.Model):
    __tablename__ = "voting_sessions"

    id = Column(CHAR(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()), nullable=False)
    title = Column(String(50), nullable=False, index=True)
    question = Column(String(255), nullable=False)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    organization_id = Column(CHAR(36), ForeignKey("organizations.id", ondelete="RESTRICT"), nullable=False, index=True)
    role_id = Column(CHAR(36), ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False, index=True)
    key_ring = Column(JSON, nullable=True, default=null)

    organization = relationship("Organization", back_populates="voting_sessions")
    options = relationship("Option", back_populates="voting_session", cascade="all, delete-orphan")
    public_keys = relationship("PublicKey", back_populates="voting_session", cascade="all, delete-orphan")
    role = relationship("Role", back_populates="voting_sessions")
    votes = relationship("Vote", back_populates="voting_session", cascade="all, delete-orphan")
    vote_submissions = relationship("VoteSubmission", back_populates="voting_session", cascade="all, delete-orphan")
    registrations = relationship("VotingSessionRegistration", back_populates="voting_session")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "question": self.question,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "organization_id": self.organization_id,
            "role_id": self.role_id,
            "key_ring": self.key_ring
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
