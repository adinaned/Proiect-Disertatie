from sqlalchemy import Column, Integer, String, Date
from src.db.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
