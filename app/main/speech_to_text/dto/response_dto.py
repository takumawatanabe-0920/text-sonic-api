from pydantic import BaseModel


class TranscribeResponseDto(BaseModel):
    audio_time: float
    speech_word_list: list[
        dict[
            str,
            float,
        ]
    ]
