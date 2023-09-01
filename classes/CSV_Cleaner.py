from typing import Any, List
from pandas import DataFrame
from dateutil.parser import parse


def is_valid_date(value: Any):
    try:
        parse(str(value), fuzzy=True, dayfirst=True)
        return True
    except ValueError:
        return False



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

    @staticmethod
    def has_clean_date(dataframe: DataFrame) -> bool:
        valid_date = dataframe['datcde'].apply(is_valid_date)
        return valid_date.bool()
