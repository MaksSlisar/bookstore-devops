from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/books/")
def create_book(title: str, author: str, price: float, year: int, db: Session = Depends(database.get_db)):
    new_book = models.Book(title=title, author=author, price=price, year=year)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books/")
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    books = db.query(models.Book).offset(skip).limit(limit).all()
    return books
