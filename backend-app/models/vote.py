from sqlalchemy import Column, Integer, String, Date, ForeignKey
from . import db


class Vote(db.Model):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("voting_sessions.id"))
    question_id = Column(Integer, ForeignKey("questions.id"))
    option_id = Column(Integer, ForeignKey("options.id"))
    token = Column(String(256))
    submission_timestamp = Column(Date)

    def to_dict(self):
        return {"id": self.id,
                "session_id": self.session_id,
                "question_id": self.question_id,
                "option_id": self.option_id,
                "token": self.token,
                "submission_timestamp": self.submission_timestamp}

    def save(self):
        db.session.add(self)
        db.session.commit()
