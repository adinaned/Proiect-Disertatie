from pydantic import BaseModel


class PublicKeyResponse(BaseModel):
    voting_session_id: str
    public_key_x: str
    public_key_y: str

    class Config:
        from_attributes = True