from datetime import datetime
from pydantic import BaseModel


class VoteResponse(BaseModel):
    id: int
    session_id: int
    question_id: int
    option_id: int
    token: str
    submission_timestamp: datetime

    class Config:
        from_attributes = True
