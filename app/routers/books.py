from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db


router = APIRouter()


@router.post("/books/", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@router.get("/books/", response_model=list[schemas.Book])
def get_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@router.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    updated_book = crud.update_book(db, book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book


@router.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    deleted_book = crud.delete_book(db, book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book
