from pydantic import BaseModel


class TranscribeSpeechWordDto(BaseModel):
    start: float
    end: float
    word: str


class TranscribeResponseDto(BaseModel):
    audio_time: float
    speech_word_list: list[TranscribeSpeechWordDto]
