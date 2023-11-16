from typing import Optional

from app.main.domain.speech_to_text.dto.response_dto import SentenceInfoDto
from app.main.infrastructure.schemas.writing_schema import TranscribeSpeechWordDto
import re


class TranscriptMapper:
    def __init__(self, speech_word_list: list[TranscribeSpeechWordDto]):
        self.speech_word_list = speech_word_list

    def map_sentences(self, sentences: list[list[str]]):
        matched_indices: set[int] = set()
        mapped_sentences: list[SentenceInfoDto] = []
        start_time = 0

        for sub_list in sentences:
            if not sub_list:
                continue

            match_index = self.__find_match_index(sub_list, 0, matched_indices)
            print(
                "match_index",
                match_index,
                "sub_list",
                sub_list,
                "start_time",
                start_time,
                "matched_indices",
                matched_indices,
            )
            if match_index is not None and match_index not in matched_indices:
                end_index = self.__find_end_index(
                    sub_list, match_index, matched_indices
                )
                print(end_index, "end_index")
                sentence_info = self.__create_sentence_info(
                    sub_list, end_index, start_time
                )
                mapped_sentences.append(sentence_info)
                if sentence_info.end_time is not None:
                    start_time = sentence_info.end_time
                matched_indices.add(match_index)
                if end_index is not None:
                    matched_indices.add(end_index)

        print(mapped_sentences, "mapped_sentences")
        return mapped_sentences

    def __is_check_partial_match(self, word1: Optional[str], word2: Optional[str]):
        if not word1 or not word2:
            return False

        # 句読点や特殊文字を除去
        cleaned_word1 = re.sub(r"[^\w\s]", "", word1.lower())
        cleaned_word2 = re.sub(r"[^\w\s]", "", word2.lower())

        return cleaned_word1 in cleaned_word2 or cleaned_word2 in cleaned_word1

    def __find_match_index(
        self, sub_list: list[str], start_index: int, matched_indices: set[int]
    ) -> Optional[int]:
        first_word = sub_list[0]
        for i in range(start_index, len(self.speech_word_list)):
            # skip already matched index
            if i in matched_indices:
                print("continue match")
                continue

            transcript = self.speech_word_list[i]
            is_partial_match = self.__is_check_partial_match(
                transcript.word, first_word
            )
            is_next_match = False
            if i + 1 < len(self.speech_word_list) and (i + 1) not in matched_indices:
                next_transcript = self.speech_word_list[i + 1]
                is_next_match = (
                    self.__is_check_partial_match(next_transcript.word, sub_list[1])
                    if len(sub_list) > 1
                    else False
                )

            if is_partial_match or is_next_match:
                return i
        return None

    def __find_end_index(
        self, sub_list: list[str], start_index: int, matched_indices: set[int]
    ) -> Optional[int]:
        last_word = sub_list[-1]
        for i in range(start_index, len(self.speech_word_list)):
            # skip already matched index
            if i in matched_indices:
                print("continue end", matched_indices, i)
                continue

            transcript = self.speech_word_list[i]
            is_partial_match = self.__is_check_partial_match(transcript.word, last_word)
            print("is_partial_match", is_partial_match, transcript.word, last_word)
            if is_partial_match:
                return i
            if i + 1 < len(self.speech_word_list) and (i + 1) not in matched_indices:
                next_transcript = self.speech_word_list[i + 1]
                print("next_transcript", next_transcript.word, last_word)
                is_next_match = self.__is_check_partial_match(
                    next_transcript.word, last_word
                )
                print("is_next_match", is_next_match)
                if is_next_match:
                    return i + 1
        return None

    def __create_sentence_info(
        self,
        sub_list: list[str],
        end_index: Optional[int],
        start_time: float,
    ) -> SentenceInfoDto:
        end_time = (
            self.speech_word_list[end_index].end
            if end_index is not None and self.speech_word_list[end_index] is not None
            else None
        )
        print(
            "end_time",
            end_time,
            "end_index",
            end_index,
        )
        return SentenceInfoDto(
            sentence=" ".join(sub_list),
            start_time=start_time,
            end_time=end_time,
        )
