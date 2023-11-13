import datetime
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship

from app.main.infrastructure.database.base import Base


class Exam(Base):
    __tablename__ = "exam"

    id = Column(String(36), primary_key=True, index=True, default=uuid.uuid4)


class User(Base):
    __tablename__ = "user"

    id = Column(String(36), primary_key=True, index=True, default=uuid.uuid4)
    encrypted_password = Column(String(255))
    email = Column(String(255), unique=True)

    writings = relationship("Writing", back_populates="user")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class Writing(Base):
    __tablename__ = "writing"

    id = Column(String(36), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(255))
    description = Column(String(5000))  # Description might have longer text
    scripts = Column(JSON, nullable=False, default=[])
    script = Column(String(5000))  # generate script from tts
    user_id = Column(String(36), ForeignKey("user.id"))
    user = relationship("User", back_populates="writings")

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
