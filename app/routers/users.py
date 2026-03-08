from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from sqlalchemy.future import select
import app.schemas, app.models 
import app.oauth2
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=app.schemas.UserResponse)
async def register(user: app.schemas.UserCreate, db: AsyncSession=Depends(get_db)):
    """
    This endpoint will register new user
    If the user already exist, return error 409
    """
    query = select(app.models.User).filter(app.models.User.email == user.email)
    result = await db.execute(query)
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")
    hashed_pwd=app.oauth2.get_password_hashed(user.password)
    new_user=app.models.User(
        name=user.name,
        email=user.email,
        password=hashed_pwd,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: AsyncSession=Depends(get_db)):
    """
    This endpoint will login users
    If the credentials are not correct, return error
    """
    query = select(app.models.User).filter(app.models.User.email == user_credentials.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not app.oauth2.verify_password(user_credentials.password, user.password): 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = app.oauth2.create_access_token(data={"user_id": user.id})
    return {
    "access_token": access_token,
    "token_type": "bearer"
}

@router.get("/me", response_model=app.schemas.UserResponse)
async def my_profile(current_user: app.models.User = Depends(app.oauth2.get_current_user)):
    """
    This endpoint retrieves the profile of the currently authenticated user.
    The identity is extracted from the JWT token.
    """
    return current_user