from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
import app.models, app.schemas, app.oauth2
from typing import List
from app.services.stripe_payment import create_payment_intent

router=APIRouter(prefix="/orders", tags=["Orders"])

from app.services.stripe_payment import create_payment_intent 

@router.post("/post_order", response_model=app.schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
async def place_order(
    db: AsyncSession=Depends(get_db), 
    current_user: app.models.User = Depends(app.oauth2.get_current_user)
    ):
    cart_query = select(app.models.CartItem).where(app.models.CartItem.user_id == current_user.id)
    cart_result = await db.execute(cart_query)
    cart_items = cart_result.scalars().all()

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Your cart is empty."
        )

    total_price = 0
    order_items_to_create = []
    
    for item in cart_items:
        product_query = select(app.models.Product).where(app.models.Product.id == item.product_id)
        product_result = await db.execute(product_query)
        product = product_result.scalars().first() 
        
        if not product or product.stock < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product {product.name if product else item.product_id} is out of stock."
            )
            
        total_price += product.price * item.quantity
        order_items_to_create.append(
            app.models.OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price
            )
        )
        product.stock -= item.quantity

    payment_data = create_payment_intent(total_price) 

    if not payment_data:
        raise HTTPException(status_code=500, detail="Payment gateway unreachable")

    new_order = app.models.Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending",
        items=order_items_to_create
    )
    
    db.add(new_order)

    for item in cart_items:
        await db.delete(item)

    await db.commit()
    await db.refresh(new_order)
    new_order.client_secret = payment_data["client_secret"]
    return new_order

@router.get("/history", response_model=List[app.schemas.OrderResponse])
async def get_my_order_history(
    db: AsyncSession = Depends(get_db),
    current_user: app.models.User = Depends(app.oauth2.get_current_user)
):
    """
    Retrieves a list of all past orders for the authenticated user
    """
    query = select(app.models.Order).where(app.models.Order.user_id == current_user.id).order_by(app.models.Order.created_at.desc())
    result = await db.execute(query)
    orders = result.scalars().all()
    
    return orders