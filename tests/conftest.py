
import pytest
import database
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True

    # Reset the in-memory store before each test for isolation
    database.items.clear()
    database.items.append({
        "id": 1, "name": "Test Item", "barcode": "123456",
        "quantity": 5, "price": 1.99, "category": "Test",
        "brand": "TestBrand", "image_url": None, "ingredients_text": None,
    })
    database._next_id = 2

    with flask_app.test_client() as c:
        yield c