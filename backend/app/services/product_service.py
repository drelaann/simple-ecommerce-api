from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """
    Сервис для работы с продуктами.
    """

    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_product(self, product_id: int) -> Product | None:
        """Получить продукт по ID."""
        return self.product_repository.get(product_id)

    def get_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Получить список всех продуктов."""
        return self.product_repository.get_all(skip=skip, limit=limit)

    def get_active_products(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Получить список активных продуктов."""
        return self.product_repository.get_active(skip=skip, limit=limit)

    def search_products(self, name: str, skip: int = 0, limit: int = 100) -> list[Product]:
        """Поиск продуктов по имени."""
        return self.product_repository.search_by_name(name, skip=skip, limit=limit)

    def create_product(self, product_create: ProductCreate) -> Product:
        """Создать новый продукт."""
        product_data = product_create.model_dump()
        return self.product_repository.create(product_data)

    def update_product(self, product_id: int, product_update: ProductUpdate) -> Product | None:
        """Обновить продукт."""
        product = self.product_repository.get(product_id)
        if not product:
            return None

        update_data = product_update.model_dump(exclude_unset=True)
        return self.product_repository.update(product, update_data)

    def delete_product(self, product_id: int) -> bool:
        """Удалить продукт."""
        return self.product_repository.delete(product_id)

    def update_stock(self, product_id: int, quantity: int) -> Product | None:
        """Обновить количество товара на складе."""
        return self.product_repository.update_stock(product_id, quantity)

