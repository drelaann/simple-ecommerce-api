from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_database_session
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


def get_user_service(db: Session = Depends(get_database_session)) -> UserService:
    """Dependency для получения UserService."""
    user_repository = UserRepository(db)
    return UserService(user_repository)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    """Создать нового пользователя."""
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/", response_model=list[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
):
    """Получить список пользователей."""
    return service.get_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Получить пользователя по ID."""
    user = service.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    """Обновить пользователя."""
    user = service.update_user(user_id, user_update)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """Удалить пользователя."""
    if not service.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

