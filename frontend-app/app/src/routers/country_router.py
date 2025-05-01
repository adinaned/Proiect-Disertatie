from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.controllers.country_controller import country_controller
from src.schemas import CountryResponse, CountryCreate, MessageResponse
from src.db.database import get_db
from . import router


@router.post("/countries", response_model=CountryResponse, operation_id="create_country")
def create_new_country_endpoint(country: CountryCreate, db: Session = Depends(get_db)):
    return country_controller.create(data=country, db=db)


@router.get("/countries", response_model=List[CountryResponse], operation_id="list_countries")
def get_countries_endpoint(db: Session = Depends(get_db)):
    return country_controller.get_all(db=db)


@router.get("/countries/{country_id}", response_model=CountryResponse, operation_id="list_country_by_id")
def get_country_by_id_endpoint(country_id: int, db: Session = Depends(get_db)):
    return country_controller.get_by_id(object_id=country_id, db=db)


@router.put("/countries/{country_id}", response_model=CountryResponse, operation_id="update_country_by_id")
def put_country_endpoint(country_id: int, country: CountryCreate, db: Session = Depends(get_db)):
    return country_controller.update(object_id=country_id, data=country, db=db)


@router.delete("/countries/{country_id}", response_model=MessageResponse, operation_id="delete_country_by_id")
def delete_country_endpoint(country_id: int, db: Session = Depends(get_db)):
    success = country_controller.delete(object_id=country_id, db=db)
    if success:
        return {"message": "Country deleted successfully"}
    return {"message": "Country not found"}
