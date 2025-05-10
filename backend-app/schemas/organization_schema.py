from pydantic import BaseModel


class OrganisationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
