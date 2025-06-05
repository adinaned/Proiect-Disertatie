from sqlalchemy import Column, Integer, String
from . import db


class PublicKey(db.Model):
    __tablename__ = 'public_keys'

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    public_key_x = Column(String(100), nullable=False)
    public_key_y = Column(String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id,
                "session_id": self.session_id,
                "user_id": self.user_id,
                "public_key_x": self.public_key_x,
                "public_key_y": self.public_key_y}

    def save(self):
        db.session.add(self)
        db.session.commit()
