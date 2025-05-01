from datetime import datetime
from pydantic import BaseModel


class VoteBase(BaseModel):
    session_id: int
    question_id: int
    option_id: int
    token: str
    submission_timestamp: datetime


class VoteCreate(VoteBase):
    pass


class VoteResponse(VoteBase):
    id: int

    class Config:
        from_attributes = True
