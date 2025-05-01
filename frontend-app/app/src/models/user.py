from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from src.db.database import Base


class User(Base):
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
