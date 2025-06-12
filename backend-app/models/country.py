from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from . import db


class Country(db.Model):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, index=True)
    name = Column(String(100), unique=True, index=True)

    users = relationship("User", back_populates="country")

    def to_dict(self):
        return {"id": self.id,
                "name": self.name}

    def save(self):
        db.session.add(self)
        db.session.commit()
