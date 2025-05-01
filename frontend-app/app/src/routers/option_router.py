from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.option_controller import option_controller
from src.schemas.option_schema import OptionResponse, OptionCreate
from src.db.database import get_db
from . import router


@router.post("/options", response_model=OptionResponse, operation_id="create_option")
def create_new_option_endpoint(option: OptionCreate, db: Session = Depends(get_db)):
    return option_controller.create(data=option, db=db)


@router.get("/options", response_model=List[OptionResponse], operation_id="list_options")
def get_options_endpoint(db: Session = Depends(get_db)):
    return option_controller.get_all(db=db)


@router.get("/options/{option_id}", response_model=OptionResponse, operation_id="list_option_by_id")
def get_option_by_id_endpoint(option_id: int, db: Session = Depends(get_db)):
    return option_controller.get_by_id(object_id=option_id, db=db)


@router.put("/options/{option_id}", response_model=OptionResponse, operation_id="update_option_by_id")
def put_option_endpoint(option_id: int, option: OptionCreate, db: Session = Depends(get_db)):
    return option_controller.update(object_id=option_id, data=option, db=db)


@router.delete("/options/{option_id}", response_model=OptionResponse, operation_id="delete_option_by_id")
def delete_option_endpoint(option_id: int, db: Session = Depends(get_db)):
    success = option_controller.delete(object_id=option_id, db=db)
    if success:
        return {"message": "Option deleted successfully"}
    return {"message": "Option not found"}
