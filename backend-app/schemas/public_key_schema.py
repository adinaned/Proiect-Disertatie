from pydantic import BaseModel


class PublicKeyResponse(BaseModel):
    id: int
    session_id: int
    user_id: int
    public_key_x: str
    public_key_y: str

    class Config:
        from_attributes = True