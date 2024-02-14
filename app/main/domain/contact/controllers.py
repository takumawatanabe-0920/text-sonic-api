from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.log.logger import logger
from app.main.domain.contact.dto.request_dto import ContactBodyDto
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.contact.services import ContactService

router = APIRouter()


@router.post("/contacts", response_model=StatusResponse)
async def contact(
    reqBody: ContactBodyDto,
    contact_service: Annotated[ContactService, Depends(ContactService)],
) -> StatusResponse:
    logger.info("controller.contact")
    return await contact_service.contact(reqBody)


@router.get("/contacts", response_model=list[ContactBodyDto])
async def get_all(contact_service: Annotated[ContactService, Depends(ContactService)]):
    return await contact_service.get_all()


@router.get("/contacts/{id_}", response_model=ContactBodyDto)
async def get_by_id(
    id_: str, contact_service: Annotated[ContactService, Depends(ContactService)]
):
    return await contact_service.get_by_id(id_)
