from pydantic import BaseModel


class OrganisationBase(BaseModel):
    name: str


class OrganisationCreate(OrganisationBase):
    pass


class OrganisationResponse(OrganisationBase):
    id: int

    class Config:
        from_attributes = True
