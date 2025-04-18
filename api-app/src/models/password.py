from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.db.database import Base

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hashed_password = Column(String(128), index=True)
    updated_at = Column(Date, index=True)
