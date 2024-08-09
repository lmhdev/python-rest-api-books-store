from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    for key, value in book.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book


def get_cart(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).first()


def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(user_id=cart.user_id)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def add_cart_item(db: Session, cart_id: int, item: schemas.CartItemCreate):
    db_item = models.CartItem(cart_id=cart_id, **item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def remove_cart_item(db: Session, item_id: int):
    db_item = db.query(models.CartItem).filter(models.CartItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item


def get_cart_items(db: Session, cart_id: int):
    return db.query(models.CartItem).filter(models.CartItem.cart_id == cart_id).all()


def create_order(db: Session, user_id: int, order: schemas.OrderCreate):
    db_order = models.Order(
        user_id=user_id, total_amount=order.total_amount, status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    for item in order.items:
        db_order_item = models.OrderItem(order_id=db_order.id, **item.model_dump())
        db.add(db_order_item)
        db.commit()
        db.refresh(db_order_item)
    return db_order


def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


def get_orders(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_order_status(db: Session, order_id: int, status: str):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order


def create_recommendation(db: Session, recommendation: schemas.RecommendationCreate):
    db_recommendation = models.Recommendation(**recommendation.model_dump())
    db.add(db_recommendation)
    db.commit()
    db.refresh(db_recommendation)
    return db_recommendation


def get_recommendations(db: Session, user_id: int, skip: int = 0, limit: int = 10):
    return (
        db.query(models.Recommendation)
        .filter(models.Recommendation.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )
