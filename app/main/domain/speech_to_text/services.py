from typing import Annotated, Optional

from fastapi import Depends, HTTPException

from app.main.domain.speech_to_text.dto.response_dto import \
    SpeechToTextResponseDto
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
    ):
        self.text_to_speech_client = text_to_speech_client
        self.writing_service = writing_service

    def convert_to_text(self, writing_id: str) -> SpeechToTextResponseDto:
        writingResponse = self.writing_service.get_writing_by_id(writing_id)
        writing = writingResponse.message
        if not writing:
            raise HTTPException(status_code=404, detail="Script not found")
        if self.__has_cached_audio(writing.scripts, writing.script):
            print("has cached audio")
            return SpeechToTextResponseDto(
                message=TranscribeResponseDto(
                    speech_word_list=writing.scripts, script=writing.script, audio_time=0  # type: ignore
                )
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
        return SpeechToTextResponseDto(message=response)

    def __has_cached_audio(self, scrips: list[dict], _script: Optional[str]) -> bool:
        for script in scrips:
            if (
                "start" in script
                and "end" in script
                and "word" in script
                and _script != None
            ):
                return True
        return False
