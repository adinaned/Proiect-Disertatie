from pydantic import BaseModel


class CountryBase(BaseModel):
    name: str


class CountryCreate(CountryBase):
    pass


class CountryResponse(CountryBase):
    id: int
