from pydantic import BaseModel


class OptionBase(BaseModel):
    name: str
    question_id: int
    session_id: int


class OptionCreate(OptionBase):
    pass


class OptionResponse(OptionBase):
    id: int

    class Config:
        from_attributes = True
