from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy.future import select
import app.models, app.schemas, app.oauth2
from typing import List

router= APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=List[app.schemas.ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    """
    Returns a list of all products in the database.
    This is a public endpoint
    """
    query=select(app.models.Product)
    result=await db.execute(query)
    products=result.scalars().all()
    return products

@router.get("/{id}", response_model=app.schemas.ProductResponse)
async def get_product_by_id(id: int, db: AsyncSession= Depends(get_db)):
    """
    Retrieves details about a specific product by it's ID
    If the product does not exist, return error 404
    """
    query=select(app.models.Product).filter(app.models.Product.id==id)
    result=await db.execute(query)
    product=result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {id} not found"
        )
    return product
        
@router.post("/categories/", response_model=app.schemas.CategoryResponse)
async def create_category(category: app.schemas.CategoryBase, db: AsyncSession = Depends(get_db)):
    new_cat = app.models.Category(name=category.name)
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat

@router.post("/", response_model=app.schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: app.schemas.ProductCreate, 
    db: AsyncSession=Depends(get_db),
    current_admin: app.models.User=Depends(app.oauth2.require_role(app.models.UserRole.admin))
    ):
    """
    Allows an Admin to add a new product. 
    Requires a valid Admin JWT token.
    """
    category_check = await db.execute(select(app.models.Category).filter(app.models.Category.id==product.category_id))
    if not category_check.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category ID does not exist"
        )
    new_product=app.models.Product(**product.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product