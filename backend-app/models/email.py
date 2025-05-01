from venv import create

from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from . import db


class Email(db.Model):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_address = Column(String(320), index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(Date)

    def to_dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "email_address": self.email_address,
                "is_verified": self.is_verified,
                "created_at": self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()