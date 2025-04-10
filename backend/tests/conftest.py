import pytest
import os
import sys
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from db.base import Base
from db.session import get_db

# Use a test database
import random


@pytest.fixture(scope="session")
def test_engine():
    """Create a test database engine."""
    # Ensure data directory exists
    os.makedirs("./data", exist_ok=True)

    random_db_name = f"test_db_{random.randint(1000, 9999)}.db"
    TEST_SQLALCHEMY_DATABASE_URL = f"sqlite:///./data/{random_db_name}"
    TEST_DB_PATH = f"./data/{random_db_name}"

    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)

    # Close all connections to the database
    engine.dispose()

    # Try to remove the database file with retries
    if os.path.exists(TEST_DB_PATH):
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                os.remove(TEST_DB_PATH)
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    time.sleep(1)  # Wait a second before trying again
                else:
                    print(
                        f"Warning: Could not remove test database file: {TEST_DB_PATH}"
                    )


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create a fresh database session for each test."""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with a test database session."""

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
