from typing import Annotated

from fastapi import Depends
from dotenv import load_dotenv
from app.core.log.logger import logger
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.contact.dto.request_dto import ContactBodyDto
from app.main.domain.mail.service import MailService
from app.main.repository.contact_repository import (
    ContactRepository,
    ContactCreate,
    ContactGet,
)

load_dotenv()


class ContactService:
    def __init__(
        self,
        mail_service: Annotated[MailService, Depends(MailService)],
        contact_repository: Annotated[ContactRepository, Depends(ContactRepository)],
    ):
        self.mail_service = mail_service
        self.contact_repository = contact_repository

    async def contact(self, args: ContactBodyDto) -> StatusResponse:
        try:
            logger.info("contact")
            # TODO: uncomment the below code
            # self.mail_service.send_message(
            #     GmailSendMessageDTO(
            #         From=args.email, Subject=args.name, Message=args.description
            #     )
            # )
            # TODO: remove the below code
            self.contact_repository.save(
                ContactCreate(
                    name=args.name,
                    email=args.email,
                    description=args.description,
                )
            )
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")

    async def get_all(self) -> list[ContactGet]:
        return self.contact_repository.get_all()

    async def get_by_id(self, id_: str) -> ContactGet | None:
        return self.contact_repository.get_by_id(id_)
