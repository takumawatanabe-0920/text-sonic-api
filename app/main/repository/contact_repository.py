from typing import Annotated, Optional

from fastapi import Depends
from sqlalchemy.future import select

from app.main.infrastructure.database.unit_of_work import UnitOfWork
from app.main.infrastructure.models import Contact
from app.main.infrastructure.schemas.contact_schema import (
    ContactCreate,
    ContactGet,
)


class ContactRepository:
    def __init__(self, uow: Annotated[UnitOfWork, Depends(UnitOfWork)]):
        self.uow = uow

    def save(self, contact: ContactCreate) -> ContactGet:
        with self.uow as uow:
            new_contact = Contact(**contact.dict())
            uow.db.add(new_contact)
            uow.db.commit()

            return ContactGet.from_orm(new_contact)

    def get_by_id(self, id_: str) -> Optional[ContactGet]:
        with self.uow as uow:
            result = uow.db.execute(select(Contact).filter(Contact.id == id_))
            contact = result.scalars().first()

            if not contact:
                return None

            return ContactGet.from_orm(contact)

    def get_all(self) -> list[ContactGet]:
        with self.uow as uow:
            result = uow.db.execute(select(Contact))
            contacts = result.scalars().all()

            return [ContactGet.from_orm(contact) for contact in contacts]
