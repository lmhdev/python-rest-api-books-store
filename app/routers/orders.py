from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas, auth
from app.database import get_db

router = APIRouter()


@router.post("/orders/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return crud.create_order(db=db, user_id=current_user.id, order=order)


@router.get("/orders/", response_model=list[schemas.Order])
def read_orders(
    skip: int = 0,
    limit: int = 10,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    orders = crud.get_orders(db, user_id=current_user.id, skip=skip, limit=limit)
    return orders


@router.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(
    order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)
):
    order = crud.update_order_status(
        db=db, order_id=order_id, status=order_update.status
    )
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
