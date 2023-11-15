from typing import Annotated, Optional

from fastapi import Depends, HTTPException

from app.core.log.logger import logger
from app.main.domain.speech_to_text.dto.response_dto import (
    SpeechToTextDto,
    SpeechToTextResponseDto,
)
from app.main.domain.speech_to_text.generate_sentence_map import (
    ProcessAndMapSentencesExecutor,
)

from app.main.domain.writings.dto.request_dto import UpdateWritingBodyDto
from app.main.domain.writings.services import WritingService
from app.main.speech_to_text.dto.response_dto import TranscribeResponseDto
from app.main.speech_to_text.stt_client import SpeechToTextClient


class SpeechToTextService:
    def __init__(
        self,
        text_to_speech_client: Annotated[
            SpeechToTextClient, Depends(SpeechToTextClient)
        ],
        writing_service: Annotated[WritingService, Depends(WritingService)],
        process_and_map_sentences_executor: Annotated[
            ProcessAndMapSentencesExecutor, Depends(ProcessAndMapSentencesExecutor)
        ],
    ):
        self.text_to_speech_client = text_to_speech_client
        self.writing_service = writing_service
        self.process_and_map_sentences_executor = process_and_map_sentences_executor

    def convert_to_text(self, writing_id: str) -> SpeechToTextResponseDto:
        logger.info("convert_to_text")
        writingResponse = self.writing_service.get_writing_by_id(writing_id)
        writing = writingResponse.message
        if not writing:
            raise HTTPException(status_code=404, detail="Script not found")
        if self.__has_cached_audio(writing.scripts, writing.script):
            logger.info("has cached audio")
            return self.__convert_response(
                TranscribeResponseDto(
                    audio_time=0,
                    script=writing.description,
                    speech_word_list=writing.scripts,  # type: ignore
                ),
                writing.description,
            )

        audio_file = "audio/" + writing_id + ".mp3"
        response = self.text_to_speech_client.transcribe(audio_file)
        self.writing_service.update_writing(
            writing_id,
            UpdateWritingBodyDto(
                title=writing.title,
                description=writing.description,
                scripts=response.speech_word_list,
                script=response.script,
            ),
        )
        logger.info("convert_to_text end")
        return self.__convert_response(response, writing.description)

    def __has_cached_audio(self, scrips: list[dict], _script: Optional[str]) -> bool:
        logger.info("has_cached_audio")
        for script in scrips:
            if (
                "start" in script
                and "end" in script
                and "word" in script
                and _script != None
            ):
                return True
        return False

    def __convert_response(
        self, response: TranscribeResponseDto, original_script: str
    ) -> SpeechToTextResponseDto:
        logger.info("convert_response")
        sentences = self.process_and_map_sentences_executor.exec(
            response.speech_word_list, original_script
        )
        return SpeechToTextResponseDto(
            message=SpeechToTextDto(
                audio_time=response.audio_time,
                script=response.script,
                sentences=sentences,
            )
        )
