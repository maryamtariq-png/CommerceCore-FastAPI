import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./commerceCore.db"

engine= create_async_engine(DATABASE_URL, echo= False, connect_args={"check_same_thread": False})

AsyncSessionLocal=async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autoflush=False, 
    autocommit= False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try: 
            yield db
        finally:
            await db.close()
            