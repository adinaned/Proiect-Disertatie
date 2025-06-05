from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.mysql import JSON

from . import db


class VotingSession(db.Model):
    __tablename__ = "voting_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False, unique=True, index=True)
    question = Column(String(255), nullable=False)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), index=True)
    key_ring = Column(JSON, nullable=True)

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "question": self.question,
                "start_datetime": self.start_datetime,
                "end_datetime": self.end_datetime,
                "role_id": self.role_id,
                "organization_id": self.organization_id,
                "key_ring": self.key_ring}

    def save(self):
        db.session.add(self)
        db.session.commit()
