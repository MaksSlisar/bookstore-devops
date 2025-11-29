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

def test_get_book_by_id(client):
    payload = {
        "title": "Test Book",
        "author": "Test Author",
        "price": 100.0,
        "year": 2024
    }
    create_response = client.post("/books/", params=payload)
    assert create_response.status_code == 200
    created = create_response.json()
    book_id = created["id"]

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == book_id
    assert data["title"] == "Test Book"

def test_delete_book(client):
    payload = {
        "title": "To Delete",
        "author": "Temp Author",
        "price": 50.0,
        "year": 2024
    }
    create_response = client.post("/books/", params=payload)
    assert create_response.status_code == 200
    book_id = create_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["detail"] == "Book deleted"

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404

