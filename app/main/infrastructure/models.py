import datetime

from sqlalchemy import Column, DateTime, String

from app.main.infrastructure.database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    encrypted_password = Column(String)
    email = Column(String, unique=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Writing(Base):
    __tablename__ = "writing"

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
