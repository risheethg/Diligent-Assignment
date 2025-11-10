"""Orders router for checkout and order management."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Request
from beanie import PydanticObjectId

from app.models.user import User
from app.models.order import Order
from app.schemas.order_schemas import OrderCreate, OrderPublic, PaymentIntentResponse, OrderItemSchema, ShippingAddressSchema
from app.security import get_current_user
from app.services.order_service import (
    create_payment_intent,
    create_order_from_cart,
    get_user_orders,
    handle_stripe_webhook
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent_endpoint(current_user: User = Depends(get_current_user)):
    """
    Create a Stripe payment intent for the current user's cart.
    Returns the client secret for the frontend to complete payment.
    """
    result = await create_payment_intent(current_user.id)
    return PaymentIntentResponse(
        clientSecret=result["clientSecret"],
        amount=result["amount"]
    )


@router.post("", response_model=OrderPublic, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create an order from the user's cart after payment confirmation.
    This should be called after the payment is successfully processed.
    """
    order = await create_order_from_cart(
        current_user.id,
        order_data.payment_intent_id,
        order_data.shipping_address
    )
    
    return OrderPublic(
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


@router.get("", response_model=List[OrderPublic])
async def get_orders(current_user: User = Depends(get_current_user)):
    """Get all orders for the current user."""
    orders = await get_user_orders(current_user.id)
    
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


@router.post("/stripe-webhook")
async def stripe_webhook(request: Request):
    """
    Webhook endpoint for Stripe events.
    This is called by Stripe to notify us of payment status changes.
    """
    payload = await request.body()
    signature = request.headers.get("stripe-signature")
    
    if not signature:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing stripe-signature header"
        )
    
    result = handle_stripe_webhook(payload, signature)
    return result
