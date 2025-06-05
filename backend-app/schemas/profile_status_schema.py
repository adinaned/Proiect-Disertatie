from datetime import datetime
from pydantic import BaseModel


class ProfileStatusResponse(BaseModel):
    id: int
    name: str
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True
