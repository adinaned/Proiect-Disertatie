from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.question_controller import question_controller
from src.schemas.question_schema import QuestionResponse, QuestionCreate
from src.db.database import get_db
from . import router


@router.post("/questions", response_model=QuestionResponse, operation_id="create_question")
def create_new_question_endpoint(question: QuestionCreate, db: Session = Depends(get_db)):
    return question_controller.create(data=question, db=db)


@router.get("/questions", response_model=List[QuestionResponse], operation_id="list_questions")
def get_questions_endpoint(db: Session = Depends(get_db)):
    return question_controller.get_all(db=db)


@router.get("/questions/{question_id}", response_model=QuestionResponse, operation_id="list_question_by_id")
def get_question_by_id_endpoint(question_id: int, db: Session = Depends(get_db)):
    return question_controller.get_by_id(object_id=question_id, db=db)


@router.put("/questions/{question_id}", response_model=QuestionResponse, operation_id="update_question_by_id")
def put_question_endpoint(question_id: int, question: QuestionCreate, db: Session = Depends(get_db)):
    return question_controller.update(object_id=question_id, data=question, db=db)


@router.delete("/questions/{question_id}", response_model=QuestionResponse, operation_id="delete_question_by_id")
def delete_question_endpoint(question_id: int, db: Session = Depends(get_db)):
    success = question_controller.delete(object_id=question_id, db=db)
    if success:
        return {"message": "Question deleted successfully"}
    return {"message": "Question not found"}
