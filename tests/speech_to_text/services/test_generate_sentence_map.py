import unittest
from app.main.domain.speech_to_text.services.generate_sentence_map import (
    TranscriptMapper,
)
from app.main.infrastructure.schemas.writing_schema import TranscribeSpeechWordDto


class TestTranscriptMapper(unittest.TestCase):
    def setUp(self):
        speech_word_list: list[TranscribeSpeechWordDto] = [
            TranscribeSpeechWordDto(word="Hello", start=0, end=1),
            TranscribeSpeechWordDto(word="world.", start=1, end=2),
            TranscribeSpeechWordDto(word="This", start=2, end=3),
            TranscribeSpeechWordDto(word="is", start=3, end=4),
            TranscribeSpeechWordDto(word="a", start=4, end=5),
            TranscribeSpeechWordDto(word="test.", start=5, end=6),
        ]
        speech_word_list2: list[TranscribeSpeechWordDto] = [
            TranscribeSpeechWordDto(word="Hello", start=0, end=1),
            TranscribeSpeechWordDto(word="world?", start=1, end=2),
            TranscribeSpeechWordDto(word="This", start=2, end=3),
            TranscribeSpeechWordDto(word="is", start=3, end=4),
            TranscribeSpeechWordDto(word="a", start=4, end=5),
            TranscribeSpeechWordDto(word="test!", start=5, end=6),
        ]
        speech_word_list3: list[TranscribeSpeechWordDto] = [
            TranscribeSpeechWordDto(word="Hello", start=0, end=1),
            TranscribeSpeechWordDto(word="world;", start=1, end=2),
            TranscribeSpeechWordDto(word="This", start=2, end=3),
            TranscribeSpeechWordDto(word="is", start=3, end=4),
            TranscribeSpeechWordDto(word="a", start=4, end=5),
            TranscribeSpeechWordDto(word="test:", start=5, end=6),
        ]
        speech_word_list4: list[TranscribeSpeechWordDto] = [
            TranscribeSpeechWordDto(word="Hello", start=0, end=1),
            TranscribeSpeechWordDto(word="world…", start=1, end=2),
            TranscribeSpeechWordDto(word="This", start=2, end=3),
            TranscribeSpeechWordDto(word="is", start=3, end=4),
            TranscribeSpeechWordDto(word="a", start=4, end=5),
            TranscribeSpeechWordDto(word="test.", start=5, end=6),
        ]

        self.mapper = TranscriptMapper(speech_word_list)
        self.mapper2 = TranscriptMapper(speech_word_list2)
        self.mapper3 = TranscriptMapper(speech_word_list3)
        self.mapper4 = TranscriptMapper(speech_word_list4)

    def test_map_sentences(self):
        sentences = [["Hello", "world."], ["This", "is", "a", "test."]]
        mapped_sentences = self.mapper.map_sentences(sentences)

        # verify length
        self.assertEqual(len(mapped_sentences), 2)

        # verify first sentence
        self.assertEqual(mapped_sentences[0].sentence, "Hello world.")
        self.assertEqual(mapped_sentences[0].start_time, 0)
        self.assertEqual(mapped_sentences[0].end_time, 2)

        # verify second sentence
        self.assertEqual(mapped_sentences[1].sentence, "This is a test.")
        self.assertEqual(mapped_sentences[1].start_time, 2)
        self.assertEqual(mapped_sentences[1].end_time, 6)

    def test_map_sentences_with_question(self):
        sentences = [["Hello", "world?"], ["This", "is", "a", "test!"]]
        mapped_sentences = self.mapper2.map_sentences(sentences)

        # verify length
        self.assertEqual(len(mapped_sentences), 2)

        # verify first sentence
        self.assertEqual(mapped_sentences[0].sentence, "Hello world?")
        self.assertEqual(mapped_sentences[0].start_time, 0)
        self.assertEqual(mapped_sentences[0].end_time, 2)

        # verify second sentence
        self.assertEqual(mapped_sentences[1].sentence, "This is a test!")
        self.assertEqual(mapped_sentences[1].start_time, 2)
        self.assertEqual(mapped_sentences[1].end_time, 6)

    def test_map_sentences_with_semicolon(self):
        sentences = [["Hello", "world;"], ["This", "is", "a", "test:"]]
        mapped_sentences = self.mapper3.map_sentences(sentences)

        # verify length
        self.assertEqual(len(mapped_sentences), 2)

        # verify first sentence
        self.assertEqual(mapped_sentences[0].sentence, "Hello world;")
        self.assertEqual(mapped_sentences[0].start_time, 0)
        self.assertEqual(mapped_sentences[0].end_time, 2)

        # verify second sentence
        self.assertEqual(mapped_sentences[1].sentence, "This is a test:")
        self.assertEqual(mapped_sentences[1].start_time, 2)
        self.assertEqual(mapped_sentences[1].end_time, 6)

    def test_map_sentences_with_ellipsis(self):
        sentences = [["Hello", "world…"], ["This", "is", "a", "test."]]
        mapped_sentences = self.mapper4.map_sentences(sentences)

        # verify length
        self.assertEqual(len(mapped_sentences), 2)

        # verify first sentence
        self.assertEqual(mapped_sentences[0].sentence, "Hello world…")
        self.assertEqual(mapped_sentences[0].start_time, 0)
        self.assertEqual(mapped_sentences[0].end_time, 2)

        # verify second sentence
        self.assertEqual(mapped_sentences[1].sentence, "This is a test.")
        self.assertEqual(mapped_sentences[1].start_time, 2)
        self.assertEqual(mapped_sentences[1].end_time, 6)


if __name__ == "__main__":
    unittest.main()
