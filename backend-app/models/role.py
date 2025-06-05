from sqlalchemy import Column, Integer, String, ForeignKey
from . import db

class Role(db.Model):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "organization_id": self.organization_id}

    def save(self):
        db.session.add(self)
        db.session.commit()
