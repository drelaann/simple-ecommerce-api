from typing import Generic, TypeVar
from sqlalchemy.orm import Session
from app.database import Base

# Переменная типа для дженериков. 
# Она позволяет создавать универсальные классы, работающие с разными типами.
ModelType = TypeVar("ModelType", bound=Base)        


class BaseRepository(Generic[ModelType]):
    """
    Базовый репозиторий с общими CRUD операциями.
    """

    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int) -> ModelType | None:
        """Получить объект по ID."""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        """Получить список объектов с пагинацией."""
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: dict) -> ModelType:
        """Создать новый объект."""
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: ModelType, obj_in: dict) -> ModelType:
        """Обновить объект."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        """Удалить объект по ID."""
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False

