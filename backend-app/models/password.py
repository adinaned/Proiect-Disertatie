from sqlalchemy import Column, Integer, String, Date, ForeignKey
from . import db

class Password(db.Model):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    password = Column(String(128), index=True)
    updated_at = Column(Date, index=True)

    def to_dict(self):
        return {"id": self.id,
                "user_id": self.user_id,
                "password": self.password,
                "updated_at": self.updated_at}

    def save(self):
        db.session.add(self)
        db.session.commit()