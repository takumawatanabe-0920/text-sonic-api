import unittest

from app.main.domain.speech_to_text.services.sentence_processor import SentenceProcessor


class TestSentenceProcessor(unittest.TestCase):
    def setUp(self):
        self.sentence_processor = SentenceProcessor()

    def test_process_sentences(self):
        original_script = "Hello, world. This is a test."
        expected_result = [["Hello,", "world."], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_question(self):
        original_script = "Hello, world? This is a test."
        expected_result = [["Hello,", "world?"], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_exclamation(self):
        original_script = "Hello, world! This is a test."
        expected_result = [["Hello,", "world!"], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_semicolon(self):
        original_script = "Hello, world; This is a test."
        expected_result = [["Hello,", "world;"], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_colon(self):
        original_script = "Hello, world: This is a test."
        expected_result = [["Hello,", "world:"], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_with_multiple_spaces(self):
        original_script = "  Hello,   world.   　This is  a   test.  　"
        expected_result = [["Hello,", "world."], ["This", "is", "a", "test."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)

    def test_process_sentences_with_no_spaces(self):
        original_script = "Hello,world.Thisisatest."
        expected_result = [["Hello,world."], ["Thisisatest."]]

        result = self.sentence_processor.process_sentences(original_script)

        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
