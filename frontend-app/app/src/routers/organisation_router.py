from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.organisation_controller import organisation_controller
from src.schemas.organisation_schema import OrganisationResponse, OrganisationCreate
from src.db.database import get_db
from . import router


@router.post("/organisations", response_model=OrganisationResponse, operation_id="create_organisation")
def create_new_organisation_endpoint(organisation: OrganisationCreate, db: Session = Depends(get_db)):
    return organisation_controller.create(data=organisation, db=db)


@router.get("/organisations", response_model=List[OrganisationResponse], operation_id="list_organisations")
def get_organisations_endpoint(db: Session = Depends(get_db)):
    return organisation_controller.get_all(db=db)


@router.get("/organisations/{organisation_id}", response_model=OrganisationResponse, operation_id="list_organisation_by_id")
def get_organisation_by_id_endpoint(organisation_id: int, db: Session = Depends(get_db)):
    return organisation_controller.get_by_id(object_id=organisation_id, db=db)


@router.put("/organisations/{organisation_id}", response_model=OrganisationResponse, operation_id="update_organisation_by_id")
def put_organisation_endpoint(organisation_id: int, organisation: OrganisationCreate, db: Session = Depends(get_db)):
    return organisation_controller.update(object_id=organisation_id, data=organisation, db=db)


@router.delete("/organisations/{organisation_id}", response_model=OrganisationResponse, operation_id="delete_organisation_by_id")
def delete_organisation_endpoint(organisation_id: int, db: Session = Depends(get_db)):
    success = organisation_controller.delete(object_id=organisation_id, db=db)
    if success:
        return {"message": "Organisation deleted successfully"}
    return {"message": "Organisation not found"}
