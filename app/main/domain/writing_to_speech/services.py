from typing import Annotated

from fastapi import Depends

from app.main.domain.writings.services import WritingService
from app.main.text_to_speech.tts_client import TextToSpeechClient
from fastapi.responses import FileResponse


class WritingToSpeechService:
    def __init__(
        self,
        writing_service: Annotated[WritingService, Depends(WritingService)],
        text_to_speech_client: Annotated[
            TextToSpeechClient, Depends(TextToSpeechClient)
        ],
    ):
        self.writing_service = writing_service
        self.text_to_speech_client = text_to_speech_client

    def convert_to_speech(self, writing_id: str) -> FileResponse:
        writing = self.writing_service.get_writing_by_id(writing_id)
        file_name = "audio/" + writing.message.id + ".mp3"
        self.text_to_speech_client.synthesize_speech(
            writing.message.description, file_name
        )
        return FileResponse(file_name, media_type="audio/mpeg")
