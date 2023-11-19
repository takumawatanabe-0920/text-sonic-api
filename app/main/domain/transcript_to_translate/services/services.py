from typing import Annotated
import asyncio
from fastapi import Depends

from app.core.log.logger import logger
from app.main.domain.transcript_to_translate.dto.request_dto import SentenceInfoDto
from app.main.domain.transcript_to_translate.dto.response_dto import (
    TranscriptToTranslateResponseDto,
    SentenceInfoDto as SentenceInfoDtoResponse,
)
from app.main.translate.translate import TranslateTextClient


class TranscriptToTranslateService:
    def __init__(
        self,
        translate_text_client: Annotated[
            TranslateTextClient, Depends(TranslateTextClient)
        ],
    ):
        self.translate_text_client = translate_text_client

    async def translate(
        self, sentences: list[SentenceInfoDto]
    ) -> TranscriptToTranslateResponseDto:
        logger.info("translate")
        translated_sentences = []
        tasks = [
            SentenceInfoDto(
                sentence=sentence.sentence,
                start_time=sentence.start_time,
                end_time=sentence.end_time,
            )
            for sentence in sentences
        ]
        print("tasks", tasks)
        translated_sentences: list[SentenceInfoDto] = (await asyncio.gather(*tasks)) or []  # type: ignore
        print("translated_sentences", translated_sentences)
        if translated_sentences:
            translated_sentences = [
                SentenceInfoDto(
                    sentence=sentence.sentence,
                    start_time=sentence.start_time,
                    end_time=sentence.end_time,
                )
                for sentence in translated_sentences
            ]
            return TranscriptToTranslateResponseDto(
                message=[
                    SentenceInfoDtoResponse(
                        sentence=sentence.sentence,
                        start_time=sentence.start_time,
                        end_time=sentence.end_time,
                    )
                    for sentence in translated_sentences
                ]
            )

        return TranscriptToTranslateResponseDto(message=[])
