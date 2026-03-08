from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
import app.models, app.schemas, app.oauth2
from typing import List

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/", response_model=app.schemas.CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    cart_item: app.schemas.CartItemCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: app.models.User = Depends(app.oauth2.get_current_user)
):
    """
    Adds a product to the user's cart
    If the item already exists, it updates the quantity
    """
    prod_query = select(app.models.Product).where(app.models.Product.id == cart_item.product_id)
    prod_result = await db.execute(prod_query)
    product = prod_result.scalars().first()

    if not product or product.stock < cart_item.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product not available or insufficient stock"
        )
    cart_query = select(app.models.CartItem).where(
        app.models.CartItem.user_id == current_user.id,
        app.models.CartItem.product_id == cart_item.product_id
    )
    cart_result = await db.execute(cart_query)
    existing_item = cart_result.scalars().first()

    if existing_item:
        existing_item.quantity += cart_item.quantity
        await db.commit()
        await db.refresh(existing_item)
        return existing_item

    new_item = app.models.CartItem(**cart_item.model_dump(), user_id=current_user.id)
    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return new_item

@router.get("/", response_model=List[app.schemas.CartItemResponse])
async def view_cart(
    db: AsyncSession = Depends(get_db),
    current_user: app.models.User = Depends(app.oauth2.get_current_user)
):
    """
    Retrieves all items in the current user's cart
    """
    query = select(app.models.CartItem).where(app.models.CartItem.user_id == current_user.id)
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_cart(
    cart_item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: app.models.User = Depends(app.oauth2.get_current_user)
):
    """Deletes a specific item from the user's cart."""
    query = select(app.models.CartItem).where(
        app.models.CartItem.id == cart_item_id, 
        app.models.CartItem.user_id == current_user.id
    )
    result = await db.execute(query)
    item = result.scalars().first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found in your cart")

    await db.delete(item)
    await db.commit()
    return None