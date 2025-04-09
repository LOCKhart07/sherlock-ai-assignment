import pytest
from fastapi import status
from .test_utils import create_test_user_data
import copy

# API base path
BASE_PATH = "/sherlock-ai/api"


def get_auth_headers(client, username, password):
    """Helper function to get authentication headers."""
    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": username,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_current_user(client):
    """Test getting current user profile."""
    # Register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Get auth token
    headers = get_auth_headers(client, user_data["username"], user_data["password"])

    # Get user profile
    response = client.get(f"{BASE_PATH}/users/me", headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Password should not be returned


def test_get_current_user_unauthorized(client):
    """Test getting current user profile without authentication."""
    response = client.get(f"{BASE_PATH}/users/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client):
    """Test getting current user profile with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get(f"{BASE_PATH}/users/me", headers=headers)
    assert response.status_code == 401


def test_update_user_profile(client):
    """Test updating user profile."""
    # Register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Get auth token
    headers = get_auth_headers(client, user_data["username"], user_data["password"])

    # Update user profile
    update_data = user_data
    update_data.pop("password")

    update_data.update(
        {
            "full_name": "Updated Name",
            "bio": "Updated bio",
            "phone": "+1234567890",
            "photo_url": "https://example.com/updated-photo.jpg",
        }
    )

    response = client.put(f"{BASE_PATH}/users/me", headers=headers, json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["bio"] == update_data["bio"]
    assert data["phone"] == update_data["phone"]
    assert data["photo_url"] == update_data["photo_url"]


def test_update_user_password(client):
    """Test updating user password."""
    # Register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Get auth token
    headers = get_auth_headers(client, user_data["username"], user_data["password"])

    # Update password
    update_data = copy.deepcopy(user_data)
    update_data.update({"password": "newpassword123", "full_name": "Updated name"})

    response = client.put(f"{BASE_PATH}/users/me", headers=headers, json=update_data)

    assert response.status_code == 200

    # Try to login with new password

    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": user_data["username"],
            "password": update_data["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200

    # Try to login with old password (should fail)

    response = client.post(
        f"{BASE_PATH}/token",
        data={
            "username": user_data["username"],
            "password": user_data["password"],
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_update_user_partial(client):
    """Test updating only some user fields."""
    # Register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Get auth token
    headers = get_auth_headers(client, user_data["username"], user_data["password"])

    # Update only bio
    update_data = copy.deepcopy(user_data)
    update_data.pop("password")

    update_data.update({"bio": "Only updating bio"})

    response = client.put(f"{BASE_PATH}/users/me", headers=headers, json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == update_data["bio"]
    assert data["full_name"] == user_data["full_name"]  # Should remain unchanged
    assert data["email"] == user_data["email"]  # Should remain unchanged


def test_update_user_invalid_email(client):
    """Test updating user with invalid email format."""
    # Register a user
    user_data = create_test_user_data()
    client.post(f"{BASE_PATH}/register", json=user_data)

    # Get auth token
    headers = get_auth_headers(client, user_data["username"], user_data["password"])

    # Try to update with invalid email
    update_data = {"email": "invalid-email"}

    response = client.put(f"{BASE_PATH}/users/me", headers=headers, json=update_data)

    assert response.status_code == 422  # Validation error
