from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.password_controller import password_controller
from src.schemas.password_schema import PasswordResponse, PasswordCreate
from src.db.database import get_db
from . import router


@router.post("/passwords", response_model=PasswordResponse, operation_id="create_password")
def create_new_password_endpoint(password: PasswordCreate, db: Session = Depends(get_db)):
    return password_controller.create(data=password, db=db)


@router.get("/passwords", response_model=List[PasswordResponse], operation_id="list_passwords")
def get_passwords_endpoint(db: Session = Depends(get_db)):
    return password_controller.get_all(db=db)


@router.get("/passwords/{password_id}", response_model=PasswordResponse, operation_id="list_password_by_id")
def get_password_by_id_endpoint(password_id: int, db: Session = Depends(get_db)):
    return password_controller.get_by_id(object_id=password_id, db=db)


@router.put("/passwords/{password_id}", response_model=PasswordResponse, operation_id="update_password_by_id")
def put_password_endpoint(password_id: int, password: PasswordCreate, db: Session = Depends(get_db)):
    return password_controller.update(object_id=password_id, data=password, db=db)


@router.delete("/passwords/{password_id}", response_model=PasswordResponse, operation_id="delete_password_by_id")
def delete_password_endpoint(password_id: int, db: Session = Depends(get_db)):
    success = password_controller.delete(object_id=password_id, db=db)
    if success:
        return {"message": "Password deleted successfully"}
    return {"message": "Password not found"}
