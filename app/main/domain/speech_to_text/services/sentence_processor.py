import re


class SentenceProcessor:
    @staticmethod
    def process_sentences(original_script: str) -> list[list[str]]:
        # Pattern for splitting sentences
        pattern = r"(?<=[.!?…;:])"
        # Split the script into sentences based on multiple ending characters
        sentences = re.split(pattern, original_script)
        # Remove empty strings and strip whitespaces
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        # Split each sentence into words
        result = [sentence.split() for sentence in sentences]
        return result
