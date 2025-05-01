from pydantic import BaseModel


class QuestionResponse(BaseModel):
    id: int
    name: str
    voting_session_id: int

    class Config:
        from_attributes = True
