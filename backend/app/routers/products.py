"""Products router for product catalog and reviews."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from beanie import PydanticObjectId

from app.models.user import User
from app.models.product import Product
from app.models.review import Review
from app.schemas.product_schemas import ProductPublic
from app.schemas.review_schemas import ReviewCreate, ReviewPublic
from app.security import get_current_user
from app.services.product_service import recalculate_product_rating

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductPublic])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    sort: Optional[str] = Query(None, regex="^(price_asc|price_desc)$"),
    q: Optional[str] = None
):
    """
    Get all products with optional filtering, sorting, and search.
    
    - **skip**: Number of products to skip (pagination)
    - **limit**: Maximum number of products to return
    - **category**: Filter by category
    - **sort**: Sort by price (price_asc or price_desc)
    - **q**: Search query (searches name and description)
    """
    # Build query
    query = {}
    
    if category:
        query = Product.find(Product.category == category)
    else:
        query = Product.find_all()
    
    # Apply text search if provided
    if q:
        # Use MongoDB text search
        query = Product.find({"$text": {"$search": q}})
    
    # Apply sorting
    if sort == "price_asc":
        query = query.sort(+Product.price)
    elif sort == "price_desc":
        query = query.sort(-Product.price)
    else:
        # Default sort by created_at descending
        query = query.sort(-Product.created_at)
    
    # Apply pagination
    products = await query.skip(skip).limit(limit).to_list()
    
    # Convert to public schema
    return [
        ProductPublic(
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
        for product in products
    ]


@router.get("/{product_id}", response_model=ProductPublic)
async def get_product(product_id: str):
    """Get a single product by ID."""
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


@router.get("/{product_id}/reviews", response_model=List[ReviewPublic])
async def get_product_reviews(product_id: str):
    """Get all reviews for a specific product."""
    try:
        reviews = await Review.find(
            Review.product_id == PydanticObjectId(product_id)
        ).sort(-Review.created_at).to_list()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Populate user names
    result = []
    for review in reviews:
        user = await User.get(review.user_id)
        user_name = f"{user.first_name} {user.last_name}" if user else "Anonymous"
        
        result.append(ReviewPublic(
            id=str(review.id),
            product_id=str(review.product_id),
            user_id=str(review.user_id),
            rating=review.rating,
            comment=review.comment,
            created_at=review.created_at,
            user_name=user_name
        ))
    
    return result


@router.post("/{product_id}/reviews", response_model=ReviewPublic, status_code=status.HTTP_201_CREATED)
async def create_review(
    product_id: str,
    review_data: ReviewCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new review for a product (requires authentication)."""
    # Verify product exists
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
    
    # Check if user already reviewed this product
    existing_review = await Review.find_one(
        Review.product_id == PydanticObjectId(product_id),
        Review.user_id == current_user.id
    )
    
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this product"
        )
    
    # Create review
    review = Review(
        product_id=PydanticObjectId(product_id),
        user_id=current_user.id,
        rating=review_data.rating,
        comment=review_data.comment
    )
    
    await review.insert()
    
    # Recalculate product rating
    await recalculate_product_rating(PydanticObjectId(product_id))
    
    return ReviewPublic(
        id=str(review.id),
        product_id=str(review.product_id),
        user_id=str(review.user_id),
        rating=review.rating,
        comment=review.comment,
        created_at=review.created_at,
        user_name=f"{current_user.first_name} {current_user.last_name}"
    )
