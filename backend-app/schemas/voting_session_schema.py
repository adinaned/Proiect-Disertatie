from datetime import datetime
from pydantic import BaseModel


class VotingSessionResponse(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    role_name: str
    organisation_id: int

    class Config:
        from_attributes = True
