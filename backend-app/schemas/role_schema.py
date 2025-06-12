from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: str
    name: str
    organization_id: str

    class Config:
        from_attributes = True
