from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

class Option(db.Model):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"))

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "session_id": self.session_id}

    def save(self):
        db.session.add(self)
        db.session.commit()