from pydantic import BaseModel


class CountryResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
