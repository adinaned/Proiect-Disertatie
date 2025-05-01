from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

class Organisation(db.Model):
    __tablename__ = "organisations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,}

    def save(self):
        db.session.add(self)
        db.session.commit()