from sqlalchemy import Column, Integer, String, Date, ForeignKey
from . import db


class VotingSession(db.Model):
    __tablename__ = "voting_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    start_time = Column(Date)
    end_time = Column(Date)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), index=True)

    def to_dict(self):
        return {"id": self.id,
                "title": self.title,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "role_id": self.role_id,
                "organisation_id": self.organisation_id}

    def save(self):
        db.session.add(self)
        db.session.commit()
