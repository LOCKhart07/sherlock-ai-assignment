import random
import string
from typing import Dict, Any


def generate_random_username(length=8):
    """Generate a random username of specified length."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def generate_random_email(username=None):
    """Generate a random email address."""
    if username is None:
        username = generate_random_username()
    return f"{username}@example.com"


def generate_random_phone():
    """Generate a random phone number."""
    return f"+1{random.randint(1000000000, 9999999999)}"


def generate_random_photo_url():
    """Generate a random photo URL."""
    return f"https://example.com/photos/{generate_random_username(10)}.jpg"


def create_test_user_data(
    username=None,
    email=None,
    password="testpass123",
    full_name="Test User",
    bio="Test bio",
    phone=None,
    photo_url=None,
) -> Dict[str, Any]:
    """Create a complete test user data dictionary."""
    if username is None:
        username = generate_random_username()
    if email is None:
        email = generate_random_email(username)
    if phone is None:
        phone = generate_random_phone()
    if photo_url is None:
        photo_url = generate_random_photo_url()

    return {
        "email": email,
        "username": username,
        "password": password,
        "full_name": full_name,
        "bio": bio,
        "phone": phone,
        "photo_url": photo_url,
    }
