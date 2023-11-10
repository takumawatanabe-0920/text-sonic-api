import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from app.main.infrastructure.database.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True, default=uuid.uuid4)
    encrypted_password = Column(String)
    email = Column(String, unique=True)

    writings = relationship("Writing", back_populates="user")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Writing(Base):
    __tablename__ = "writing"

    id = Column(String, primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String)
    description = Column(String)

    user_id = Column(String, ForeignKey("user.id"))
    user = relationship("User", back_populates="writings")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
