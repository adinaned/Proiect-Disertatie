from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    country_id: int
    city: str
    address: str
    national_id: int
    organization_id: str
    role_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
