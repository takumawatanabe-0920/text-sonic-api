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
        self, sentences: list[SentenceInfoDto], target_language: str
    ) -> TranscriptToTranslateResponseDto:
        logger.info("translate")
        print("sentences", sentences)
        translated_sentences = []
        tasks = [
            self.translate_text_client.translate(sentence.sentence, target_language)
            for sentence in sentences
        ]
        translated_sentences: list[str] = await asyncio.gather(*tasks)

        sentence_info_list: list[SentenceInfoDtoResponse] = []
        for index, sentence in enumerate(sentences):
            translated_sentence = translated_sentences[index]
            translated_sentence_info = SentenceInfoDtoResponse(
                sentence=translated_sentence,
                start_time=sentence.start_time,
                end_time=sentence.end_time,
            )
            sentence_info_list.append(translated_sentence_info)

        return TranscriptToTranslateResponseDto(message=sentence_info_list)
