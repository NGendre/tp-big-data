from typing import Any, List

import pandas as pd
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
    def clean_double_quote_if_not_empty(words: List[str]) -> None:
        for (index, word) in enumerate(words):
            if word != "" and word[0] == '"' and word[-1] == '"':
                word = word[1:]
                word = word[:-1]
                words[index] = word

    @staticmethod
    def has_clean_date(dataframe: DataFrame) -> bool:
        valid_date = dataframe['datcde'].apply(is_valid_date)
        return valid_date.bool()

    @staticmethod
    def is_between_years(dataframe: DataFrame,startYear:int,endYear:int) -> bool:
        date = int(pd.to_datetime(dataframe['datcde']).dt.year)
        if date>=startYear and date<=endYear:
            return True
        return False



