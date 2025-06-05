from datetime import datetime
from pydantic import BaseModel


class VotingSessionResponse(BaseModel):
    id: int
    title: str
    question: str
    start_datetime: datetime
    end_datetime: datetime
    role_id: int
    organization_id: int
    key_ring: dict | None = None

    class Config:
        from_attributes = True
