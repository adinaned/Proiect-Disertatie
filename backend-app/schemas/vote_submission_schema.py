from pydantic import BaseModel


class VoteSubmissionResponse(BaseModel):
    id: str
    voting_session_id: str

    class Config:
        from_attributes = True
