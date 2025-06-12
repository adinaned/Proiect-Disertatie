from datetime import datetime
from pydantic import BaseModel
from typing import Union


class VoteResponse(BaseModel):
    id: str
    voting_session_id: str
    option_id: str
    token: str
    key_image: Union[str, dict]
    ring_hash: str
    signature: Union[str, dict]
    submission_timestamp: datetime

    class Config:
        from_attributes = True
