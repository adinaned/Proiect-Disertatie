from datetime import datetime
from pydantic import BaseModel


class PasswordBase(BaseModel):
    user_id: int
    hashed_password: str
    updated_at: datetime


class PasswordCreate(PasswordBase):
    pass


class PasswordResponse(PasswordBase):
    id: int

    class Config:
        from_attributes = True
