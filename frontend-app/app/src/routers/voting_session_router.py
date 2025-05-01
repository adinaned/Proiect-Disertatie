from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.voting_session_controller import voting_session_controller
from src.schemas.voting_session_schema import VotingSessionResponse, VotingSessionCreate
from src.db.database import get_db
from . import router


@router.post("/voting_sessions", response_model=VotingSessionResponse, operation_id="create_voting_session")
def create_new_voting_session_endpoint(voting_session: VotingSessionCreate, db: Session = Depends(get_db)):
    return voting_session_controller.create(data=voting_session, db=db)


@router.get("/voting_sessions", response_model=List[VotingSessionResponse], operation_id="list_voting_sessions")
def get_voting_sessions_endpoint(db: Session = Depends(get_db)):
    return voting_session_controller.get_all(db=db)


@router.get("/voting_sessions/{voting_session_id}", response_model=VotingSessionResponse, operation_id="list_voting_session_by_id")
def get_voting_session_by_id_endpoint(voting_session_id: int, db: Session = Depends(get_db)):
    return voting_session_controller.get_by_id(object_id=voting_session_id, db=db)


@router.put("/voting_sessions/{voting_session_id}", response_model=VotingSessionResponse, operation_id="update_voting_session_by_id")
def put_voting_session_endpoint(voting_session_id: int, voting_session: VotingSessionCreate, db: Session = Depends(get_db)):
    return voting_session_controller.update(object_id=voting_session_id, data=voting_session, db=db)


@router.delete("/voting_sessions/{voting_session_id}", response_model=VotingSessionResponse, operation_id="delete_voting_session_by_id")
def delete_voting_session_endpoint(voting_session_id: int, db: Session = Depends(get_db)):
    success = voting_session_controller.delete(object_id=voting_session_id, db=db)
    if success:
        return {"message": "VotingSession deleted successfully"}
    return {"message": "VotingSession not found"}
