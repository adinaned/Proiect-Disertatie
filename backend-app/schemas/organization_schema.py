from pydantic import BaseModel


class OrganizationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
