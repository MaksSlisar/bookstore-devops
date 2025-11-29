from tests.conftest import TestingSessionLocal
from .test_data import create_fake_books

def test_read_books_empty(client):
    response = client.get("/books/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_book(client):
    payload = {
        "title": "Test Book",
        "author": "Test Author",
        "price": 100.0,
        "year": 2024
    }
    response = client.post("/books/", params=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Book"
    assert data["author"] == "Test Author"

def test_read_books_with_data(client):
    db = TestingSessionLocal()
    create_fake_books(db, count=5)
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
