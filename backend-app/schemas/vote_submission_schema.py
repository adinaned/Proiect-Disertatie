from pydantic import BaseModel


class VoteSubmissionResponse(BaseModel):
    id: int
    session_id: int
    has_voted: bool

    class Config:
        from_attributes = True
