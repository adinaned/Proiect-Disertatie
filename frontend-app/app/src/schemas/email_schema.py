from datetime import datetime
from pydantic import BaseModel

class EmailBase(BaseModel):
    user_id: int
    email_address: str
    is_verified: bool
    created_at: datetime


class EmailCreate(EmailBase):
    pass


class EmailResponse(EmailBase):
    pass
