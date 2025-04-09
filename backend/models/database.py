from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    bio = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    google_id = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)
