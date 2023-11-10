from fastapi import Depends
from sqlalchemy.orm import Session

from app.main.infrastructure.base import get_db


class UnitOfWork:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.db.rollback()
        else:
            self.db.commit()
