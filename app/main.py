from fastapi import FastAPI
from app.routers import users, books, cart, orders, recommendations
from app.models import User, Book, Cart, CartItem, Order, OrderItem, Recommendation
from app.database import engine, Base


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(books.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(recommendations.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Store API"}
