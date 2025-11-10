"""Cart router for shopping cart management."""
from fastapi import APIRouter, Depends, status

from app.models.user import User
from app.schemas.cart_schemas import CartItemCreate, CartPublic, CartItemUpdate
from app.security import get_current_user
from app.services.cart_service import (
    get_populated_cart,
    add_item_to_cart,
    update_cart_item,
    remove_item_from_cart
)

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("", response_model=CartPublic)
async def get_cart(current_user: User = Depends(get_current_user)):
    """Get the current user's cart with populated product details."""
    return await get_populated_cart(current_user.id)


@router.post("/items", response_model=CartPublic, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user)
):
    """Add an item to the cart."""
    await add_item_to_cart(current_user.id, item)
    return await get_populated_cart(current_user.id)


@router.put("/items/{product_id}", response_model=CartPublic)
async def update_cart_item_quantity(
    product_id: str,
    item_update: CartItemUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update the quantity of an item in the cart."""
    await update_cart_item(current_user.id, product_id, item_update.quantity)
    return await get_populated_cart(current_user.id)


@router.delete("/items/{product_id}", response_model=CartPublic)
async def remove_from_cart(
    product_id: str,
    current_user: User = Depends(get_current_user)
):
    """Remove an item from the cart."""
    await remove_item_from_cart(current_user.id, product_id)
    return await get_populated_cart(current_user.id)
