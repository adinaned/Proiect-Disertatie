from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.mysql import JSON

from . import db


class Vote(db.Model):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    token = Column(String(256))
    key_image = Column(String(256), nullable=True)
    ring_hash = Column(String(256), nullable=True)
    signature = Column(JSON, nullable=True)
    submission_timestamp = Column(Date)

    def to_dict(self):
        return {"id": self.id,
                "session_id": self.session_id,
                "option_id": self.option_id,
                "token": self.token,
                "key_image": self.key_image,
                "ring_hash": self.ring_hash,
                "signature": self.signature,
                "submission_timestamp": self.submission_timestamp}

    def save(self):
        db.session.add(self)
        db.session.commit()
