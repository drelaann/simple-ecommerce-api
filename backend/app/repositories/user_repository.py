from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    Репозиторий для работы с пользователями.
    """

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> User | None:
        """Получить пользователя по username."""
        return self.db.query(User).filter(User.username == username).first()

    def is_active(self, user: User) -> bool:
        """Проверить, активен ли пользователь."""
        return user.is_active

