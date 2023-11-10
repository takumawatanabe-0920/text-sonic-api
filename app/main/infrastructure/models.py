from sqlalchemy import Column, DateTime, String, func

from app.main.infrastructure.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    encrypted_password = Column(String)
    email = Column(String, unique=True)

    # created_at = Column(DateTime, default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())


class Writing(Base):
    __tablename__ = "writing"

    id = Column(String, primary_key=True)
    title = Column(String)
    description = Column(String)

    # created_at = Column(DateTime, default=func.now())
    # updated_at = Column(DateTime, onupdate=func.now())
