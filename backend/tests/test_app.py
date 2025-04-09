import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app, get_db
from models import Base
import random
import string

# API base path
BASE_PATH = "/sherlock-ai/api"

# Create test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


# Helper function to generate random usernames
def generate_random_username(length=8):
    """Generate a random username of specified length."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


@pytest.fixture(autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)


def test_register_user_success():
    username = generate_random_username()
    email = f"{username}@email.com"
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email,
            "username": username,
            "password": "testpass123",
            "full_name": "Test User",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"


def test_register_user_duplicate_email():
    username1 = generate_random_username()
    username2 = generate_random_username()
    email = f"{username1}@email.com"

    # First registration
    client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email,
            "username": username1,
            "password": "testpass123",
            "full_name": "Test User 1",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )

    # Try to register with same email
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email,
            "username": username2,
            "password": "testpass123",
            "full_name": "Test User 2",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"


def test_register_user_duplicate_username():
    username = generate_random_username()
    email1 = f"{username}@email.com"
    email2 = f"{generate_random_username()}@email.com"

    # First registration
    client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email1,
            "username": username,
            "password": "testpass123",
            "full_name": "Test User 1",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )

    # Try to register with same username
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email2,
            "username": username,
            "password": "testpass123",
            "full_name": "Test User 2",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"


def test_register_user_invalid_email():
    username = generate_random_username()
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": "invalid-email",
            "username": username,
            "password": "testpass123",
            "full_name": "Test User",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 422  # Validation error


def test_register_user_missing_required_fields():
    username = generate_random_username()
    email = f"{username}@email.com"
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email,
            "username": username,
            # Missing password and other required fields
        },
    )
    assert response.status_code == 422  # Validation error
