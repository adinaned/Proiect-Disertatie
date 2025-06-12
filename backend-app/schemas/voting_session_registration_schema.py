from pydantic import BaseModel


class VotingSessionRegistrationResponse(BaseModel):
    voting_session_id: str
    user_id: str

    class Config:
        from_attributes = True
