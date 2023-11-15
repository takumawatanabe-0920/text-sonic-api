from app.main.domain.speech_to_text.dto.response_dto import SentenceInfoDto
from app.main.domain.speech_to_text.services.generate_sentence_map import (
    TranscriptMapper,
)
from app.main.domain.speech_to_text.services.sentence_processor import SentenceProcessor
from app.main.infrastructure.schemas.writing_schema import TranscribeSpeechWordDto


class ProcessAndMapSentencesExecutor:
    @staticmethod
    def exec(
        speech_word_list: list[TranscribeSpeechWordDto], original_script: str
    ) -> list[SentenceInfoDto]:
        sentences = SentenceProcessor.process_sentences(original_script)
        return TranscriptMapper(speech_word_list).map_sentences(sentences)
