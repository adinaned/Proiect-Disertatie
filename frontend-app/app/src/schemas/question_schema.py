from pydantic import BaseModel


class QuestionBase(BaseModel):
    name: str
    voting_session_id: int


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True
