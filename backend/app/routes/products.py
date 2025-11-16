from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.dependencies import get_database_session
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService
from app.schemas.product import Product, ProductCreate, ProductUpdate

router = APIRouter()


def get_product_service(db: Session = Depends(get_database_session)) -> ProductService:
    """Dependency для получения ProductService."""
    product_repository = ProductRepository(db)
    return ProductService(product_repository)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    """Создать новый продукт."""
    return service.create_product(product)


@router.get("/", response_model=list[Product])
def read_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    active_only: bool = Query(False),
    search: str = Query(None),
    service: ProductService = Depends(get_product_service),
):
    """Получить список продуктов."""
    if search:
        return service.search_products(search, skip=skip, limit=limit)
    if active_only:
        return service.get_active_products(skip=skip, limit=limit)
    return service.get_products(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=Product)
def read_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Получить продукт по ID."""
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден",
        )
    return product


@router.put("/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    """Обновить продукт."""
    product = service.update_product(product_id, product_update)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден",
        )
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service),
):
    """Удалить продукт."""
    if not service.delete_product(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден",
        )


@router.patch("/{product_id}/stock", response_model=Product)
def update_stock(
    product_id: int,
    quantity: int = Query(..., ge=0),
    service: ProductService = Depends(get_product_service),
):
    """Обновить количество товара на складе."""
    product = service.update_stock(product_id, quantity)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Продукт не найден",
        )
    return product

