from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.email_controller import email_controller
from src.schemas.email_schema import EmailResponse, EmailCreate
from src.db.database import get_db
from . import router


@router.post("/emails", response_model=EmailResponse, operation_id="create_email")
def create_new_email_endpoint(email: EmailCreate, db: Session = Depends(get_db)):
    return email_controller.create(data=email, db=db)


@router.get("/emails", response_model=List[EmailResponse], operation_id="list_emails")
def get_emails_endpoint(db: Session = Depends(get_db)):
    return email_controller.get_all(db=db)


@router.get("/emails/{email_id}", response_model=EmailResponse, operation_id="list_email_by_id")
def get_email_by_id_endpoint(email_id: int, db: Session = Depends(get_db)):
    return email_controller.get_by_id(object_id=email_id, db=db)


@router.put("/emails/{email_id}", response_model=EmailResponse, operation_id="update_email_by_id")
def put_email_endpoint(email_id: int, email: EmailCreate, db: Session = Depends(get_db)):
    return email_controller.update(object_id=email_id, data=email, db=db)


@router.delete("/emails/{email_id}", response_model=EmailResponse, operation_id="delete_email_by_id")
def delete_email_endpoint(email_id: int, db: Session = Depends(get_db)):
    success = email_controller.delete(object_id=email_id, db=db)
    if success:
        return {"message": "Email deleted successfully"}
    return {"message": "Email not found"}
