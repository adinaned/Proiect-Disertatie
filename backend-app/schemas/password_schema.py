from datetime import datetime
from pydantic import BaseModel


class PasswordResponse(BaseModel):
    id: int
    user_id: int
    hashed_password: str
    updated_at: datetime

    class Config:
        from_attributes = True
