import re
from typing import Annotated

from fastapi import Depends, HTTPException
from langdetect import detect
from word2number import w2n

from app.core.log.logger import logger
from app.main.domain.common.dto.response_dto import StatusResponse
from app.main.domain.writings.dto.request_dto import (CreateWritingBodyDto,
                                                      UpdateWritingBodyDto)
from app.main.domain.writings.dto.response_dto import (WritingDto,
                                                       WritingResponse,
                                                       WritingsResponse)
from app.main.infrastructure.schemas.writing_schema import (
    TranscribeSpeechWordDto, WritingCreate, WritingGet, WritingUpdate)
from app.main.repository.writing_repository import WritingRepository

# list of number words
number_words = (
    r"(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|"
    r"thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|"
    r"twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|"
    r"thousand|million|billion|"
    r"first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|"
    r"eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|"
    r"seventeenth|eighteenth|nineteenth|twentieth|thirtieth|"
    r"fortieth|fiftieth|sixtieth|seventieth|eightieth|ninetieth)"
)


class WritingService:
    def __init__(
        self,
        writing_repository: Annotated[WritingRepository, Depends(WritingRepository)],
    ):
        self.__writing_repository = writing_repository

    def get_writings(self, user_id) -> WritingsResponse:
        writings = self.__writing_repository.get_all(user_id)
        return self.__convert_list_response(writings)

    def get_writing_by_id(self, id_: str) -> WritingResponse:
        writing = self.__writing_repository.get_by_id(id_)
        if not writing:
            raise HTTPException(status_code=404, detail="Script not found")

        return WritingResponse(
            message=WritingDto(
                id=writing.id,
                title=writing.title,
                description=writing.description,
                user_id=writing.user_id,
                scripts=writing.scripts,
                script=writing.script,
                created_at=writing.created_at,
                updated_at=writing.updated_at,
            )
        )

    def create_writing(
        self, __user_id: str, writing: CreateWritingBodyDto
    ) -> WritingResponse:
        # raise HTTPException(status_code=404, detail="Script not found")
        if self.__is_english(writing.description) == False:
            raise HTTPException(
                status_code=400, detail="Script description is not english"
            )

        if self.__check_length(writing.description) == False:
            raise HTTPException(
                status_code=400, detail="Script description length is too long"
            )

        description = self.__transform_to_speech_description(writing.description)

        created_writing = self.__writing_repository.save(
            WritingCreate(
                title=writing.title,
                description=description,
                user_id=__user_id,
            )
        )
        if not created_writing:
            raise HTTPException(status_code=404, detail="Script not found")

        return self.get_writing_by_id(created_writing.id)

    def update_writing(
        self, id_: str, writing: UpdateWritingBodyDto
    ) -> WritingResponse:
        if self.__is_english(writing.description) == False:
            raise HTTPException(
                status_code=400, detail="Script description is not english"
            )

        if self.__check_length(writing.description) == False:
            raise HTTPException(
                status_code=400, detail="Script description length is too long"
            )

        description = self.__transform_to_speech_description(writing.description)

        updated_writing = self.__writing_repository.update(
            id_,
            WritingUpdate(
                title=writing.title,
                description=description,
                script=writing.script,
                scripts=[
                    TranscribeSpeechWordDto.from_orm(script)
                    for script in writing.scripts or []
                ],
            ),
        )

        if not updated_writing:
            raise HTTPException(status_code=404, detail="Script not found")

        return self.get_writing_by_id(id_)

    def delete_writing(self, id_: str, user_id: str) -> StatusResponse:
        try:
            self.__writing_repository.delete(id_, user_id)
            return StatusResponse(message="OK")
        # pylint: disable=broad-exception-caught
        except Exception as e:
            logger.error(e)
            return StatusResponse(message="NG")

    def __convert_list_response(self, writings: list[WritingGet]) -> WritingsResponse:
        return WritingsResponse(
            message=[
                WritingDto(
                    id=writing.id,
                    title=writing.title,
                    description=writing.description,
                    scripts=writing.scripts,
                    script=writing.script,
                    user_id=writing.user_id,
                    created_at=writing.created_at,
                    updated_at=writing.updated_at,
                )
                for writing in writings
            ]
        )

    # length check
    def __check_length(self, description: str) -> bool:
        # remove space
        description = description.replace(" ", "")
        # remove new line
        description = description.replace("\n", "")
        length = len(description)
        if length > 1000:
            return False

        return True

    def __transform_to_speech_description(self, description: str) -> str:
        removeSpace = description.replace("　", " ")
        partConvertNumber = self.__word_to_num(removeSpace)
        removeHyphen = partConvertNumber.replace("-", " ")

        return removeHyphen

    def __word_to_num(self, description: str) -> str:
        number_pattern = r"\b({0})(\s{0})+\b".format(number_words)
        # Replace the number words with the corresponding numbers
        new_description = re.sub(
            number_pattern,
            lambda m: "-".join(m.group().split()),
            description,
            flags=re.IGNORECASE,
        )
        words = new_description.split(" ")
        print("words", words)
        pattern = r"[.,;:?!()\[\]{}'\"”“’‘]"
        # Remove the special characters from each word
        words = [re.sub(pattern, "", word) for word in words]
        for word in words:
            try:
                num = w2n.word_to_num(word)
                new_description = replace_with_numbers(new_description, word, num)
            except ValueError:
                pass

        return new_description

    def __is_english(self, description: str) -> bool:
        try:
            lang = detect(description)
            if lang == "en":
                return True
            else:
                return False
        except Exception:
            return False


def replace_with_numbers(text, word, num):
    return re.sub(r"\b{}\b".format(word), str(num), text, flags=re.IGNORECASE)
