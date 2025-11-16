from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db


def get_database_session(db: Session = Depends(get_db)) -> Session:
    """
    Dependency для получения сессии базы данных.
    """
    return db

