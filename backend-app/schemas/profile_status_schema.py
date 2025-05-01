from datetime import datetime
from pydantic import BaseModel


class ProfileStatusResponse(BaseModel):
    id: int
    name: str
    updated_at: datetime

    class Config:
        from_attributes = True
