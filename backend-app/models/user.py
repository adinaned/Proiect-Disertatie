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
    organisation_id = Column(Integer, ForeignKey("organisations.id"))
    profile_status_id = Column(Integer, ForeignKey("profile_statuses.id"))
    created_at = Column(Date)

    email = relationship("Email")
    country = relationship("Country")
    role = relationship("Role")
    organisation = relationship("Organisation")
    profile_status = relationship("ProfileStatus")

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
                "organisation_id": self.organisation_id,
                "profile_status_id": self.profile_status_id,
                "created_at": self.created_at}

    def save(self):
        db.session.add(self)
        db.session.commit()
