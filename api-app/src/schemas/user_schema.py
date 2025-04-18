from pydantic import BaseModel
from datetime import date


class UserBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    country_id: int
    city: str
    address: str
    national_id: int
    role_id: int
    organisation_id: int
    profile_status_id: int


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True
