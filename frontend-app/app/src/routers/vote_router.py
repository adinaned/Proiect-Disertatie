from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.vote_controller import vote_controller
from src.schemas.vote_schema import VoteResponse, VoteCreate
from src.db.database import get_db
from . import router


@router.post("/votes", response_model=VoteResponse, operation_id="create_vote")
def create_new_vote_endpoint(vote: VoteCreate, db: Session = Depends(get_db)):
    return vote_controller.create(data=vote, db=db)


@router.get("/votes", response_model=List[VoteResponse], operation_id="list_votes")
def get_votes_endpoint(db: Session = Depends(get_db)):
    return vote_controller.get_all(db=db)


@router.get("/votes/{vote_id}", response_model=VoteResponse, operation_id="list_vote_by_id")
def get_vote_by_id_endpoint(vote_id: int, db: Session = Depends(get_db)):
    return vote_controller.get_by_id(object_id=vote_id, db=db)


@router.put("/votes/{vote_id}", response_model=VoteResponse, operation_id="update_vote_by_id")
def put_vote_endpoint(vote_id: int, vote: VoteCreate, db: Session = Depends(get_db)):
    return vote_controller.update(object_id=vote_id, data=vote, db=db)


@router.delete("/votes/{vote_id}", response_model=VoteResponse, operation_id="delete_vote_by_id")
def delete_vote_endpoint(vote_id: int, db: Session = Depends(get_db)):
    success = vote_controller.delete(object_id=vote_id, db=db)
    if success:
        return {"message": "Vote deleted successfully"}
    return {"message": "Vote not found"}
