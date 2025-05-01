from datetime import datetime
from pydantic import BaseModel


class ProfileStatusBase(BaseModel):
    name: str
    updated_at: datetime


class ProfileStatusCreate(ProfileStatusBase):
    pass


class ProfileStatusResponse(ProfileStatusBase):
    id: int

    class Config:
        from_attributes = True
