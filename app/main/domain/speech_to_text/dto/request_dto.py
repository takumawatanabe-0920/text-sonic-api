from pydantic import BaseModel
from google.cloud import texttospeech


class WritingToSpeechBodyDto(BaseModel):
    gender: texttospeech.SsmlVoiceGender
