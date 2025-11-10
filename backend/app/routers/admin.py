"""Admin router for administrative functions."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.schemas.product_schemas import ProductCreate, ProductUpdate, ProductPublic
from app.schemas.order_schemas import OrderPublic, OrderItemSchema, ShippingAddressSchema
from app.security import get_current_admin_user
from app.services.order_service import get_all_orders

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_current_admin_user)])


@router.post("/products", response_model=ProductPublic, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_admin_user)
):
    """Create a new product (admin only)."""
    product = Product(
        name=product_data.name,
        description=product_data.description,
        price=product_data.price,
        imageUrl=product_data.imageUrl,
        category=product_data.category,
        stock_quantity=product_data.stock_quantity
    )
    
    await product.insert()
    
    return ProductPublic(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        imageUrl=product.imageUrl,
        category=product.category,
        stock_quantity=product.stock_quantity,
        avg_rating=product.avg_rating,
        review_count=product.review_count,
        created_at=product.created_at
    )


@router.put("/products/{product_id}", response_model=ProductPublic)
async def update_product(
    product_id: str,
    product_data: ProductUpdate,
    current_user: User = Depends(get_current_admin_user)
):
    """Update a product (admin only)."""
    try:
        product = await Product.get(PydanticObjectId(product_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update fields if provided
    update_data = product_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(product, field, value)
    
    await product.save()
    
    return ProductPublic(
        id=str(product.id),
        name=product.name,
        description=product.description,
        price=product.price,
        imageUrl=product.imageUrl,
        category=product.category,
        stock_quantity=product.stock_quantity,
        avg_rating=product.avg_rating,
        review_count=product.review_count,
        created_at=product.created_at
    )


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_admin_user)
):
    """Delete a product (admin only)."""
    try:
        product = await Product.get(PydanticObjectId(product_id))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    await product.delete()
    return None


@router.get("/orders", response_model=List[OrderPublic])
async def get_all_orders_admin(current_user: User = Depends(get_current_admin_user)):
    """Get all orders across the platform (admin only)."""
    orders = await get_all_orders()
    
    return [
        OrderPublic(
            id=str(order.id),
            user_id=str(order.user_id),
            items=[
                OrderItemSchema(
                    product_id=str(item.product_id),
                    name=item.name,
                    price=item.price,
                    quantity=item.quantity
                )
                for item in order.items
            ],
            total_amount=order.total_amount,
            shipping_address=ShippingAddressSchema(
                street=order.shipping_address.street,
                city=order.shipping_address.city,
                state=order.shipping_address.state,
                zip_code=order.shipping_address.zip_code
            ),
            status=order.status,
            stripe_payment_intent_id=order.stripe_payment_intent_id,
            created_at=order.created_at
        )
        for order in orders
    ]
