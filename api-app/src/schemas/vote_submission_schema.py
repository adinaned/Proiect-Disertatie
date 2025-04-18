from pydantic import BaseModel


class VoteSubmissionBase(BaseModel):
    session_id: int
    has_voted: bool


class VoteSubmissionCreate(VoteSubmissionBase):
    pass


class VoteSubmissionResponse(VoteSubmissionBase):
    id: int

    class Config:
        from_attributes = True
