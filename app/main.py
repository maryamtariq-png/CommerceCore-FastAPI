from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, products, orders, cart
import uvicorn

app = FastAPI(
    title="CommerceCore API",
    description="A high-performance asynchronous e-commerce backend",
    version="1.0.0"
)

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to CommerceCore API",
        "docs": "/docs",
        "status": "online"
    }
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)