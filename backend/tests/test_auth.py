import pytest
from fastapi import status
from .test_utils import (
    generate_random_username,
    generate_random_email,
    create_test_user_data,
)

# API base path
BASE_PATH = "/sherlock-ai/api"


def test_register_user_success(client):
    """Test successful user registration."""
    user_data = create_test_user_data()
    response = client.post(f"{BASE_PATH}/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_register_user_duplicate_email(client):
    """Test registration with duplicate email."""
    username1 = generate_random_username()
    username2 = generate_random_username()
    email = generate_random_email(username1)

    # First registration
    user_data1 = create_test_user_data(username=username1, email=email)
    client.post(f"{BASE_PATH}/register", json=user_data1)

    # Try to register with same email
    user_data2 = create_test_user_data(username=username2, email=email)
    response = client.post(f"{BASE_PATH}/register", json=user_data2)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"


def test_register_user_duplicate_username(client):
    """Test registration with duplicate username."""
    username = generate_random_username()
    email1 = generate_random_email(username)
    email2 = generate_random_email()

    # First registration
    user_data1 = create_test_user_data(username=username, email=email1)
    client.post(f"{BASE_PATH}/register", json=user_data1)

    # Try to register with same username
    user_data2 = create_test_user_data(username=username, email=email2)
    response = client.post(f"{BASE_PATH}/register", json=user_data2)

    assert response.status_code == 400
    assert response.json()["detail"] == "Username or email already registered"


def test_register_user_invalid_email(client):
    """Test registration with invalid email format."""
    username = generate_random_username()
    user_data = create_test_user_data(username=username, email="invalid-email")
    response = client.post(f"{BASE_PATH}/register", json=user_data)
    assert response.status_code == 422  # Validation error


def test_register_user_missing_required_fields(client):
    """Test registration with missing required fields."""
    username = generate_random_username()
    email = generate_random_email(username)
    response = client.post(
        f"{BASE_PATH}/register",
        json={
            "email": email,
            "username": username,
            # Missing password and other required fields
        },
    )
    assert response.status_code == 422  # Validation error


def test_login_success(client):
    """Test successful login."""
    # First register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Then try to login
    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data


def test_login_wrong_password(client):
    """Test login with wrong password."""
    # First register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Then try to login with wrong password
    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": user_data["username"],
            "password": "wrongpassword",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_nonexistent_user(client):
    """Test login with nonexistent user."""
    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": "nonexistentuser",
            "password": "anypassword",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_google_auth_invalid_token(client):
    """Test Google authentication with invalid token."""
    response = client.post(f"{BASE_PATH}/google", json={"token": "invalid_token"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate Google credentials"
