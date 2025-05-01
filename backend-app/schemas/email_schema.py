from datetime import datetime
from pydantic import BaseModel


class EmailResponse(BaseModel):
    id: int
    user_id: int
    email_address: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True
