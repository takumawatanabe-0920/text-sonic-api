import re


class SentenceProcessor:
    @staticmethod
    def process_sentences(original_script: str) -> list[list[str]]:
        # replace abbreviations
        temp_marker = "TEMP_MARKER"
        abbreviations = [
            r"Mr\.",
            r"Mrs\.",
            r"Ms\.",
            r"Dr\.",
            r"Prof\.",
            r"No\.",
            r"Vol\.",
            r"p\.m\.",
            r"a\.m\.",
            r"e\.g\.",
            r"i\.e\.",
            r"U\.S\.A\.",
        ]
        for abbr in abbreviations:
            original_script = re.sub(
                abbr,
                lambda match: match.group().replace(".", temp_marker),
                original_script,
            )

        # separate sentences
        sentences = re.split(r"(?<=[.!?…;:])", original_script)
        # back to original
        sentences = [sentence.replace(temp_marker, ".") for sentence in sentences]

        # trim
        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
        # split
        result = [sentence.split() for sentence in sentences]
        return result
