from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.role_controller import role_controller
from src.schemas.role_schema import RoleResponse, RoleCreate
from src.db.database import get_db
from . import router


@router.post("/roles", response_model=RoleResponse, operation_id="create_role")
def create_new_role_endpoint(role: RoleCreate, db: Session = Depends(get_db)):
    return role_controller.create(data=role, db=db)


@router.get("/roles", response_model=List[RoleResponse], operation_id="list_roles")
def get_roles_endpoint(db: Session = Depends(get_db)):
    return role_controller.get_all(db=db)


@router.get("/roles/{role_id}", response_model=RoleResponse, operation_id="list_role_by_id")
def get_role_by_id_endpoint(role_id: int, db: Session = Depends(get_db)):
    return role_controller.get_by_id(object_id=role_id, db=db)


@router.put("/roles/{role_id}", response_model=RoleResponse, operation_id="update_role_by_id")
def put_role_endpoint(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    return role_controller.update(object_id=role_id, data=role, db=db)


@router.delete("/roles/{role_id}", response_model=RoleResponse, operation_id="delete_role_by_id")
def delete_role_endpoint(role_id: int, db: Session = Depends(get_db)):
    success = role_controller.delete(object_id=role_id, db=db)
    if success:
        return {"message": "Role deleted successfully"}
    return {"message": "Role not found"}
