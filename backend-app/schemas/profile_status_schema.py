from datetime import datetime
from pydantic import BaseModel


class ProfileStatusResponse(BaseModel):
    id: str
    name: str
    user_id: str
    updated_at: datetime

    class Config:
        from_attributes = True
