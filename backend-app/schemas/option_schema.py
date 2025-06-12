from pydantic import BaseModel


class OptionResponse(BaseModel):
    id: str
    name: str
    voting_session_id: str

    class Config:
        from_attributes = True
