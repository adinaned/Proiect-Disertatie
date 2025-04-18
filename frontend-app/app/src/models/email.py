from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from src.db.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    email_address = Column(String(320), index=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(Date)