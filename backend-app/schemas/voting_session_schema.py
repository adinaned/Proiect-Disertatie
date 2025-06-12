from datetime import datetime
from pydantic import BaseModel


class VotingSessionResponse(BaseModel):
    id: str
    title: str
    question: str
    start_datetime: datetime
    end_datetime: datetime
    organization_id: str
    role_id: str
    key_ring: dict | None = None

    class Config:
        from_attributes = True
