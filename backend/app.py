from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
from api import auth

from db.session import get_db, engine
from db.base import Base
from models.user import User
from schemas.user import UserCreate, UserInDB, Token, UserResponse
from core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Create database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(max_request_body_size=10 * 1024 * 1024)  # 10MB

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
def ping():
    return {"message": "pong"}


@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(auth.router, tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000)
