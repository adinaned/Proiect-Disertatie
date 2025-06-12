from datetime import datetime
from pydantic import BaseModel


class PasswordResponse(BaseModel):
    id: str
    user_id: str
    password: str
    updated_at: datetime

    class Config:
        from_attributes = True
