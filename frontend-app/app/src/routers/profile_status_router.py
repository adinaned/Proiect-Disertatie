from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.profile_status_controller import profile_status_controller
from src.schemas.profile_status_schema import ProfileStatusResponse, ProfileStatusCreate
from src.db.database import get_db
from . import router


@router.post("/profile_statuses", response_model=ProfileStatusResponse, operation_id="create_profile_status")
def create_new_profile_status_endpoint(profile_status: ProfileStatusCreate, db: Session = Depends(get_db)):
    return profile_status_controller.create(data=profile_status, db=db)


@router.get("/profile_statuses", response_model=List[ProfileStatusResponse], operation_id="list_profile_statuses")
def get_profile_statuses_endpoint(db: Session = Depends(get_db)):
    return profile_status_controller.get_all(db=db)


@router.get("/profile_statuses/{profile_status_id}", response_model=ProfileStatusResponse, operation_id="list_profile_status_by_id")
def get_profile_status_by_id_endpoint(profile_status_id: int, db: Session = Depends(get_db)):
    return profile_status_controller.get_by_id(object_id=profile_status_id, db=db)


@router.put("/profile_statuses/{profile_status_id}", response_model=ProfileStatusResponse, operation_id="update_profile_status_by_id")
def put_profile_status_endpoint(profile_status_id: int, profile_status: ProfileStatusCreate, db: Session = Depends(get_db)):
    return profile_status_controller.update(object_id=profile_status_id, data=profile_status, db=db)


@router.delete("/profile_statuses/{profile_status_id}", response_model=ProfileStatusResponse, operation_id="delete_profile_status_by_id")
def delete_profile_status_endpoint(profile_status_id: int, db: Session = Depends(get_db)):
    success = profile_status_controller.delete(object_id=profile_status_id, db=db)
    if success:
        return {"message": "ProfileStatus deleted successfully"}
    return {"message": "ProfileStatus not found"}
