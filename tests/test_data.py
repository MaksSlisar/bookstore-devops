from faker import Faker
from app.models import Book
from app.database import Base
from sqlalchemy.orm import Session

fake = Faker("uk_UA")

def generate_fake_book() -> dict:
    return {
        "title": fake.sentence(nb_words=3),
        "author": fake.name(),
        "price": round(fake.pyfloat(left_digits=2, right_digits=2, positive=True), 2),
        "year": fake.year()
    }

def create_fake_books(db: Session, count: int = 10):
    books = []
    for _ in range(count):
        data = generate_fake_book()
        book = Book(
            title=data["title"],
            author=data["author"],
            price=data["price"],
            year=data["year"],
        )
        db.add(book)
        books.append(book)
    db.commit()
    return books
