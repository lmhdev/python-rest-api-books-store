from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas, auth
from app.database import get_db


router = APIRouter()


@router.post("/cart/", response_model=schemas.Cart)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)):
    return crud.create_cart(db=db, cart=cart)


@router.get("/cart/", response_model=schemas.Cart)
def read_cart(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart = crud.get_cart(db, user_id=current_user.id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("/cart/items/", response_model=schemas.CartItem)
def add_item_to_cart(
    item: schemas.CartItemCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart = crud.get_cart(db, user_id=current_user.id)
    if cart is None:
        cart = crud.create_cart(db=db, cart=schemas.CartCreate(user_id=current_user.id))
    return crud.add_cart_item(db=db, cart_id=cart.id, item=item)


@router.delete("/cart/items/{item_id}", response_model=schemas.CartItem)
def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    item = crud.remove_cart_item(db=db, item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/cart/items/", response_model=list[schemas.CartItem])
def read_cart_items(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    cart = crud.get_cart(db, user_id=current_user.id)
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    items = crud.get_cart_items(db=db, cart_id=cart.id)
    return items
