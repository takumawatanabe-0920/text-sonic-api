import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException
from fastapi.responses import FileResponse

from app.main.domain.writings.services import WritingService
from app.main.text_to_speech.tts_client import TextToSpeechClient
from app.main.utils.cloud_storage import CloudStorageLib, DownloadMp3BodyDto


class WritingToSpeechService:
    def __init__(
        self,
        writing_service: Annotated[WritingService, Depends(WritingService)],
        text_to_speech_client: Annotated[
            TextToSpeechClient, Depends(TextToSpeechClient)
        ],
        cloud_storage_lib: Annotated[CloudStorageLib, Depends(CloudStorageLib)],
    ):
        self.writing_service = writing_service
        self.text_to_speech_client = text_to_speech_client
        self.cloud_storage_lib = cloud_storage_lib

    async def convert_to_speech(self, writing_id: str) -> FileResponse:
        writing = self.writing_service.get_writing_by_id(writing_id)
        file_name = "audio/" + writing.message.id + ".mp3"
        try:
            # bytesデータをファイルに保存して、FileResponseで返す
            mp3_data = await self.cloud_storage_lib.download_mp3_data(
                DownloadMp3BodyDto(bucket_name="text-sonic-speechs", source=file_name)
            )
            audio_file = self.__get_audio_file(file_name, mp3_data)
            if audio_file:
                return audio_file
        except:
            print("file does not exist, so we will create a new file and return it.")
            pass

        audio_data = await self.text_to_speech_client.synthesize_speech(
            writing.message.description, file_name
        )
        audio_file = self.__get_audio_file(file_name, audio_data)

        if not audio_file:
            raise HTTPException(status_code=500, detail="audio file is not found")

        return audio_file

    def __get_audio_file(self, file_name: str, data: bytes) -> Optional[FileResponse]:
        with open(file_name, "wb") as f:
            f.write(data)

        if os.path.isfile(file_name):
            print("file exists")
            return FileResponse(file_name, media_type="audio/mpeg")
