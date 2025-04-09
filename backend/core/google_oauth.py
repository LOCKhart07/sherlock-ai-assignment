from typing import Optional
from fastapi import HTTPException, status
from google.oauth2 import id_token
from google.auth.transport import requests
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, UTC

from models.user import User
from core.config import GOOGLE_CLIENT_ID


async def verify_google_token(token: str, db: Session) -> Optional[User]:
    try:
        idinfo = None
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), GOOGLE_CLIENT_ID
            )
        except ValueError as e:
            # Check if the error is related to timing
            if "Token used too early" in str(e):
                # Allow for a small clock skew
                idinfo = id_token.verify_oauth2_token(
                    token, requests.Request(), GOOGLE_CLIENT_ID
                )
        if not idinfo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Google credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Get user info from token
        userid = idinfo["sub"]
        email = idinfo["email"]
        name = idinfo.get("name", "")
        picture = idinfo.get("picture", "")

        # Check if user exists
        user = db.query(User).filter(User.email == email).first()

        if not user:
            # Create new user if doesn't exist
            user = User(
                email=email,
                username=email.split("@")[0],  # Use email prefix as username
                full_name=name,
                photo_url=picture,
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    except ValueError as e:
        print("Invalid authentication credentials" + str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
