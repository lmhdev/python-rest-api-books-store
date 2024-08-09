from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str


class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    price: float
    isbn: Optional[str] = None


class BookUpdate(BaseModel):
    title: str
    author: str
    description: str
    price: float
    isbn: Optional[str] = None


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    price: float
    isbn: Optional[str]

    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    book_id: int
    quantity: int
    price: float


class CartItemCreate(CartItemBase):
    pass


class CartItem(CartItemBase):
    id: int

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    user_id: int


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    id: int
    items: list[CartItem] = []

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    book_id: int
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    total_amount: float
    status: str


class OrderCreate(OrderBase):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: str


class Order(OrderBase):
    id: int
    user_id: int
    items: list[OrderItem] = []

    class Config:
        from_attributes = True


class RecommendationBase(BaseModel):
    user_id: int
    book_id: int
    reason: str


class RecommendationCreate(RecommendationBase):
    pass


class Recommendation(RecommendationBase):
    id: int

    class Config:
        from_attributes = True
