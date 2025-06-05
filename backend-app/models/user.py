from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from . import db


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), index=True)
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    country_id = Column(Integer, ForeignKey("countries.id"))
    city = Column(String(256))
    address = Column(String(256))
    national_id = Column(Integer)
    role_id = Column(Integer, ForeignKey("roles.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    created_at = Column(Date)

    email = relationship("Email")
    country = relationship("Country")
    role = relationship("Role")
    organization = relationship("Organization")

    def to_dict(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "date_of_birth": self.date_of_birth,
                "country_id": self.country_id,
                "city": self.city,
                "address": self.address,
                "national_id": self.national_id,
                "role_id": self.role_id,
                "organization_id": self.organization_id,
                "created_at": self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()
