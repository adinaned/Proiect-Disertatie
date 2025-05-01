from pydantic import BaseModel


class OptionResponse(BaseModel):
    id: int
    name: str
    question_id: int
    session_id: int

    class Config:
        from_attributes = True
