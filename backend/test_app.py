import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app, get_db
from models import Base

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


@pytest.fixture(autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)


def test_register_user_success():
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["full_name"] == "Test User"
    assert data["bio"] == "Test bio"
    assert data["phone"] == "1234567890"
    assert data["photo_url"] == "https://example.com/photo.jpg"


def test_register_user_duplicate_email():
    # First registration
    client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser1",
            "password": "testpass123",
            "full_name": "Test User 1",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )

    # Try to register with same email
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser2",
            "password": "testpass123",
            "full_name": "Test User 2",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_register_user_duplicate_username():
    # First registration
    client.post(
        "/register",
        json={
            "email": "test1@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User 1",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )

    # Try to register with same username
    response = client.post(
        "/register",
        json={
            "email": "test2@example.com",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User 2",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already taken"


def test_register_user_invalid_email():
    response = client.post(
        "/register",
        json={
            "email": "invalid-email",
            "username": "testuser",
            "password": "testpass123",
            "full_name": "Test User",
            "bio": "Test bio",
            "phone": "1234567890",
            "photo_url": "https://example.com/photo.jpg",
        },
    )
    assert response.status_code == 422  # Validation error


def test_register_user_missing_required_fields():
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            # Missing password and other required fields
        },
    )
    assert response.status_code == 422  # Validation error
