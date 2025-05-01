from typing import Type, TypeVar, Optional
from sqlalchemy.orm import Session, class_mapper
from pydantic import BaseModel
from sqlalchemy.sql.operators import eq

T = TypeVar('T')


class BaseController:
    def __init__(self, model: Type[T], schema_create: Type[BaseModel], schema_response: Type[BaseModel]):
        self.model = model
        self.schema_create = schema_create
        self.schema_response = schema_response

    def create(self, data: BaseModel, db: Session) -> BaseModel:
        new_object = self.model(**data.model_dump())
        db.add(new_object)
        db.commit()
        db.refresh(new_object)

        obj_dict = self._sqlalchemy_to_dict(new_object)
        return self.schema_response(**obj_dict)

    def get_all(self, db: Session) -> list[BaseModel]:
        objects = db.query(self.model).all()
        return [self.schema_response(**self._sqlalchemy_to_dict(obj)) for obj in objects]

    def get_by_id(self, object_id: int, db: Session) -> Optional[BaseModel]:
        obj = db.query(self.model).filter(eq(self.model.id, object_id)).first()
        if obj:
            obj_dict = self._sqlalchemy_to_dict(obj)
            return self.schema_response(**obj_dict)
        return None

    def update(self, object_id: int, data: BaseModel, db: Session) -> Optional[BaseModel]:
        db_object = db.query(self.model).filter(eq(self.model.id, object_id)).first()
        if db_object:
            for key, value in data.model_dump().items():
                setattr(db_object, key, value)
            db.commit()
            db.refresh(db_object)

            obj_dict = self._sqlalchemy_to_dict(db_object)
            return self.schema_response(**obj_dict)
        return None

    def delete(self, object_id: int, db: Session) -> bool:
        db_object = db.query(self.model).filter(eq(self.model.id, object_id)).first()
        if db_object:
            db.delete(db_object)
            db.commit()
            return True
        return False

    def _sqlalchemy_to_dict(self, obj):
        return {column.name: getattr(obj, column.name) for column in class_mapper(self.model).columns}
