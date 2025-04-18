from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.vote_submission_controller import vote_submission_controller
from src.schemas.vote_submission_schema import VoteSubmissionResponse, VoteSubmissionCreate
from src.db.database import get_db
from . import router


@router.post("/vote_submissions", response_model=VoteSubmissionResponse, operation_id="create_vote_submission")
def create_new_vote_submission_endpoint(vote_submission: VoteSubmissionCreate, db: Session = Depends(get_db)):
    return vote_submission_controller.create(data=vote_submission, db=db)


@router.get("/vote_submissions", response_model=List[VoteSubmissionResponse], operation_id="list_vote_submissions")
def get_vote_submissions_endpoint(db: Session = Depends(get_db)):
    return vote_submission_controller.get_all(db=db)


@router.get("/vote_submissions/{vote_submission_id}", response_model=VoteSubmissionResponse, operation_id="list_vote_submission_by_id")
def get_vote_submission_by_id_endpoint(vote_submission_id: int, db: Session = Depends(get_db)):
    return vote_submission_controller.get_by_id(object_id=vote_submission_id, db=db)


@router.put("/vote_submissions/{vote_submission_id}", response_model=VoteSubmissionResponse, operation_id="update_vote_submission_by_id")
def put_vote_submission_endpoint(vote_submission_id: int, vote_submission: VoteSubmissionCreate, db: Session = Depends(get_db)):
    return vote_submission_controller.update(object_id=vote_submission_id, data=vote_submission, db=db)


@router.delete("/vote_submissions/{vote_submission_id}", response_model=VoteSubmissionResponse, operation_id="delete_vote_submission_by_id")
def delete_vote_submission_endpoint(vote_submission_id: int, db: Session = Depends(get_db)):
    success = vote_submission_controller.delete(object_id=vote_submission_id, db=db)
    if success:
        return {"message": "VoteSubmission deleted successfully"}
    return {"message": "VoteSubmission not found"}
