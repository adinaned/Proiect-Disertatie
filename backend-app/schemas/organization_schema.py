from pydantic import BaseModel


class OrganizationResponse(BaseModel):
    id: str
    name: str

    class Config:
        from_attributes = True
