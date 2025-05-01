from sqlalchemy import Column, Integer, Boolean, ForeignKey
from . import db

class VoteSubmission(db.Model):
    __tablename__ = "vote_submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"), index=True)
    has_voted = Column(Boolean, default=False)

    def to_dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "session_id": self.session_id,
                "has_voted": self.has_voted}

    def save(self):
        db.session.add(self)
        db.session.commit()
