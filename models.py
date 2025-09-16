from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def get_utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    author = Column(String, nullable=False)
    game = Column(String, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=get_utc_now)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    text = Column(String)
    timestamp = Column(DateTime(timezone=True), default=get_utc_now)
