from typing import List


class LineCleaner:
    @staticmethod
    def delimit(line: str, delimiter: str) -> List[str]:
        line = line.strip()
        return line.split(delimiter)

    @staticmethod
    def clean_double_quote(words: List[str]) -> None:
        for (index, word) in enumerate(words):
            if word[0] == '"' and word[-1] == '"':
                word = word[1:]
                word = word[:-1]
                words[index] = word

