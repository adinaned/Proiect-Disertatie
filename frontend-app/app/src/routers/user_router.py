from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.user_controller import user_controller
from src.schemas.user_schema import UserResponse, UserCreate
from src.db.database import get_db
from . import router


@router.post("/users", response_model=UserResponse, operation_id="create_user")
def create_new_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.create(data=user, db=db)


@router.get("/users", response_model=List[UserResponse], operation_id="list_users")
def get_users_endpoint(db: Session = Depends(get_db)):
    return user_controller.get_all(db=db)


@router.get("/users/{user_id}", response_model=UserResponse, operation_id="list_user_by_id")
def get_user_by_id_endpoint(user_id: int, db: Session = Depends(get_db)):
    return user_controller.get_by_id(object_id=user_id, db=db)


@router.put("/users/{user_id}", response_model=UserResponse, operation_id="update_user_by_id")
def put_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    return user_controller.update(object_id=user_id, data=user, db=db)


@router.delete("/users/{user_id}", response_model=UserResponse, operation_id="delete_user_by_id")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    success = user_controller.delete(object_id=user_id, db=db)
    if success:
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}
