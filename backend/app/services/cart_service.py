"""Cart service for business logic."""
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId
from fastapi import HTTPException, status

from app.models.cart import Cart, CartItem
from app.models.product import Product
from app.schemas.cart_schemas import CartItemCreate, CartPublic, CartItemPublic, ProductInCart


async def get_user_cart(user_id: PydanticObjectId) -> Cart:
    """
    Get the user's cart. Creates a new cart if one doesn't exist.
    """
    cart = await Cart.find_one(Cart.user_id == user_id)
    
    if not cart:
        cart = Cart(user_id=user_id, items=[])
        await cart.insert()
    
    return cart


async def add_item_to_cart(user_id: PydanticObjectId, item: CartItemCreate) -> Cart:
    """
    Add an item to the user's cart or update quantity if it already exists.
    """
    # Verify product exists and has sufficient stock
    product = await Product.get(PydanticObjectId(item.product_id))
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.stock_quantity < item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {product.stock_quantity} available."
        )
    
    # Get or create cart
    cart = await get_user_cart(user_id)
    
    # Check if item already exists in cart
    existing_item = None
    for cart_item in cart.items:
        if str(cart_item.product_id) == item.product_id:
            existing_item = cart_item
            break
    
    if existing_item:
        # Update quantity
        new_quantity = existing_item.quantity + item.quantity
        
        if product.stock_quantity < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Only {product.stock_quantity} available."
            )
        
        existing_item.quantity = new_quantity
    else:
        # Add new item
        cart.items.append(CartItem(
            product_id=PydanticObjectId(item.product_id),
            quantity=item.quantity
        ))
    
    cart.updated_at = datetime.utcnow()
    await cart.save()
    
    return cart


async def update_cart_item(user_id: PydanticObjectId, product_id: str, quantity: int) -> Cart:
    """
    Update the quantity of a specific item in the cart.
    """
    # Verify product exists and has sufficient stock
    product = await Product.get(PydanticObjectId(product_id))
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock. Only {product.stock_quantity} available."
        )
    
    cart = await get_user_cart(user_id)
    
    # Find and update the item
    item_found = False
    for cart_item in cart.items:
        if str(cart_item.product_id) == product_id:
            cart_item.quantity = quantity
            item_found = True
            break
    
    if not item_found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    
    cart.updated_at = datetime.utcnow()
    await cart.save()
    
    return cart


async def remove_item_from_cart(user_id: PydanticObjectId, product_id: str) -> Cart:
    """
    Remove an item from the user's cart.
    """
    cart = await get_user_cart(user_id)
    
    # Filter out the item
    original_length = len(cart.items)
    cart.items = [item for item in cart.items if str(item.product_id) != product_id]
    
    if len(cart.items) == original_length:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found in cart"
        )
    
    cart.updated_at = datetime.utcnow()
    await cart.save()
    
    return cart


async def get_populated_cart(user_id: PydanticObjectId) -> CartPublic:
    """
    Get the user's cart with full product details populated.
    """
    cart = await get_user_cart(user_id)
    
    # Populate product details for each item
    populated_items = []
    total = 0.0
    
    for cart_item in cart.items:
        product = await Product.get(cart_item.product_id)
        
        if product:
            product_in_cart = ProductInCart(
                id=str(product.id),
                name=product.name,
                price=product.price,
                imageUrl=product.imageUrl,
                stock_quantity=product.stock_quantity
            )
            
            populated_item = CartItemPublic(
                product_id=str(cart_item.product_id),
                quantity=cart_item.quantity,
                product=product_in_cart
            )
            
            populated_items.append(populated_item)
            total += product.price * cart_item.quantity
    
    return CartPublic(
        id=str(cart.id),
        user_id=str(cart.user_id),
        items=populated_items,
        total=round(total, 2)
    )


async def clear_cart(user_id: PydanticObjectId) -> None:
    """
    Clear all items from the user's cart.
    """
    cart = await get_user_cart(user_id)
    cart.items = []
    cart.updated_at = datetime.utcnow()
    await cart.save()
