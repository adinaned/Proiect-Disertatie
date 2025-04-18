from datetime import datetime
from pydantic import BaseModel


class VotingSessionBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    role_name: str
    organisation_id: int


class VotingSessionCreate(VotingSessionBase):
    pass


class VotingSessionResponse(VotingSessionBase):
    id: int

    class Config:
        from_attributes = True
