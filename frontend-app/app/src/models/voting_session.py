from sqlalchemy import Column, Integer, String, Date, ForeignKey
from src.db.database import Base


class VotingSession(Base):
    __tablename__ = "voting_sessions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    start_time = Column(Date)
    end_time = Column(Date)
    role_id = Column(Integer, ForeignKey("roles.id"), index=True)
    organisation_id = Column(Integer, ForeignKey("organisations.id"), index=True)

    def refresh(self, db_vote):
        pass

    def commit(self):
        pass

    def add(self, db_vote):
        pass
