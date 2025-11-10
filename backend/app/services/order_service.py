"""Order service for business logic."""
from typing import Optional
from beanie import PydanticObjectId
from fastapi import HTTPException, status
import stripe

from app.config import settings
from app.models.order import Order, OrderItem, ShippingAddress
from app.models.product import Product
from app.services.cart_service import get_user_cart, clear_cart
from app.schemas.order_schemas import ShippingAddressSchema

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


async def create_payment_intent(user_id: PydanticObjectId) -> dict:
    """
    Create a Stripe payment intent based on the user's cart.
    Returns the client secret for the frontend.
    """
    # Get user's cart
    cart = await get_user_cart(user_id)
    
    if not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total amount
    total_amount = 0.0
    
    for cart_item in cart.items:
        product = await Product.get(cart_item.product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {cart_item.product_id} not found"
            )
        
        # Check stock availability
        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}. Only {product.stock_quantity} available."
            )
        
        total_amount += product.price * cart_item.quantity
    
    # Convert to cents for Stripe
    amount_in_cents = int(total_amount * 100)
    
    try:
        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency="usd",
            metadata={
                "user_id": str(user_id)
            }
        )
        
        return {
            "clientSecret": payment_intent.client_secret,
            "amount": total_amount
        }
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stripe error: {str(e)}"
        )


async def create_order_from_cart(
    user_id: PydanticObjectId,
    payment_intent_id: str,
    shipping_address: ShippingAddressSchema
) -> Order:
    """
    Create an order from the user's cart after successful payment.
    This should be called after payment confirmation.
    """
    # Get user's cart
    cart = await get_user_cart(user_id)
    
    if not cart.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Prepare order items and calculate total
    order_items = []
    total_amount = 0.0
    
    for cart_item in cart.items:
        product = await Product.get(cart_item.product_id)
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {cart_item.product_id} not found"
            )
        
        # Check and decrease stock
        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for {product.name}"
            )
        
        product.stock_quantity -= cart_item.quantity
        await product.save()
        
        # Create order item with snapshot of product data
        order_item = OrderItem(
            product_id=cart_item.product_id,
            name=product.name,
            price=product.price,
            quantity=cart_item.quantity
        )
        
        order_items.append(order_item)
        total_amount += product.price * cart_item.quantity
    
    # Create the order
    order = Order(
        user_id=user_id,
        items=order_items,
        total_amount=round(total_amount, 2),
        shipping_address=ShippingAddress(
            street=shipping_address.street,
            city=shipping_address.city,
            state=shipping_address.state,
            zip_code=shipping_address.zip_code
        ),
        status="pending",
        stripe_payment_intent_id=payment_intent_id
    )
    
    await order.insert()
    
    # Clear the cart
    await clear_cart(user_id)
    
    return order


async def get_user_orders(user_id: PydanticObjectId) -> list[Order]:
    """
    Get all orders for a specific user.
    """
    orders = await Order.find(Order.user_id == user_id).sort(-Order.created_at).to_list()
    return orders


async def get_all_orders() -> list[Order]:
    """
    Get all orders (admin function).
    """
    orders = await Order.find_all().sort(-Order.created_at).to_list()
    return orders


async def update_order_status(order_id: PydanticObjectId, status: str) -> Optional[Order]:
    """
    Update the status of an order.
    """
    order = await Order.get(order_id)
    
    if not order:
        return None
    
    order.status = status
    await order.save()
    return order


def handle_stripe_webhook(payload: bytes, signature: str) -> dict:
    """
    Handle Stripe webhook events.
    This processes payment status updates from Stripe.
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
    
    # Handle the event
    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        # Payment was successful
        # You could update order status here if needed
        print(f"Payment succeeded for PaymentIntent: {payment_intent['id']}")
    
    elif event["type"] == "payment_intent.payment_failed":
        payment_intent = event["data"]["object"]
        # Payment failed
        print(f"Payment failed for PaymentIntent: {payment_intent['id']}")
    
    return {"status": "success"}
