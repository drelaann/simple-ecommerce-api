from sqlalchemy.orm import Session
from app.models.product import Product
from app.repositories.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """
    Репозиторий для работы с продуктами.
    """

    def __init__(self, db: Session):
        super().__init__(Product, db)

    def get_active(self, skip: int = 0, limit: int = 100) -> list[Product]:
        """Получить список активных продуктов."""
        return (
            self.db.query(Product)
            .filter(Product.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> list[Product]:
        """Поиск продуктов по имени."""
        return (
            self.db.query(Product)
            .filter(Product.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_stock(self, product_id: int, quantity: int) -> Product | None:
        """Обновить количество товара на складе."""
        product = self.get(product_id)
        if product:
            product.stock = quantity
            self.db.commit()
            self.db.refresh(product)
            return product
        return None

