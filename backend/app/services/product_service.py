"""Product service for business logic."""
from typing import Optional
from beanie import PydanticObjectId
from app.models.product import Product
from app.models.review import Review


async def recalculate_product_rating(product_id: PydanticObjectId) -> None:
    """
    Recalculate and update the average rating and review count for a product.
    This should be called after a new review is added or a review is deleted.
    """
    # Get the product
    product = await Product.get(product_id)
    
    if not product:
        return
    
    # Get all reviews for this product
    reviews = await Review.find(Review.product_id == product_id).to_list()
    
    if not reviews:
        # No reviews, reset to defaults
        product.avg_rating = 0.0
        product.review_count = 0
    else:
        # Calculate average rating
        total_rating = sum(review.rating for review in reviews)
        product.avg_rating = round(total_rating / len(reviews), 2)
        product.review_count = len(reviews)
    
    # Save the updated product
    await product.save()


async def get_product_by_id(product_id: str) -> Optional[Product]:
    """Get a product by its ID."""
    try:
        return await Product.get(PydanticObjectId(product_id))
    except Exception:
        return None


async def decrease_stock(product_id: PydanticObjectId, quantity: int) -> bool:
    """
    Decrease the stock quantity of a product.
    Returns True if successful, False if insufficient stock.
    """
    product = await Product.get(product_id)
    
    if not product:
        return False
    
    if product.stock_quantity < quantity:
        return False
    
    product.stock_quantity -= quantity
    await product.save()
    return True
