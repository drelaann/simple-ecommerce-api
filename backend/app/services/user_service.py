from passlib.context import CryptContext

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """
    Сервис для работы с пользователями.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверить пароль."""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Хешировать пароль."""
        return pwd_context.hash(password)

    def get_user(self, user_id: int) -> User | None:
        """Получить пользователя по ID."""
        return self.user_repository.get(user_id)

    def get_user_by_email(self, email: str) -> User | None:
        """Получить пользователя по email."""
        return self.user_repository.get_by_email(email)

    def get_user_by_username(self, username: str) -> User | None:
        """Получить пользователя по username."""
        return self.user_repository.get_by_username(username)

    def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Получить список пользователей."""
        return self.user_repository.get_all(skip=skip, limit=limit)

    def create_user(self, user_create: UserCreate) -> User:
        """Создать нового пользователя."""
        # Проверка на существование пользователя
        if self.user_repository.get_by_email(user_create.email):
            raise ValueError("Пользователь с таким email уже существует")
        if self.user_repository.get_by_username(user_create.username):
            raise ValueError("Пользователь с таким username уже существует")

        # Хеширование пароля
        hashed_password = self.get_password_hash(user_create.password)

        # Создание пользователя
        user_data = user_create.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password

        return self.user_repository.create(user_data)

    def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        """Обновить пользователя."""
        user = self.user_repository.get(user_id)
        if not user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        # Если обновляется пароль, нужно его захешировать
        if "password" in update_data:
            update_data["hashed_password"] = self.get_password_hash(update_data.pop("password"))

        return self.user_repository.update(user, update_data)

    def delete_user(self, user_id: int) -> bool:
        """Удалить пользователя."""
        return self.user_repository.delete(user_id)

    def authenticate_user(self, username: str, password: str) -> User | None:
        """Аутентификация пользователя."""
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

