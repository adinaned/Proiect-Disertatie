from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

class Question(db.Model):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), index=True)
    voting_session_id = Column(Integer, ForeignKey("voting_sessions.id"), index=True)

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "voting_session_id": self.voting_session_id}

    def save(self):
        db.session.add(self)
        db.session.commit()
