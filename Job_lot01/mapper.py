#!/usr/bin/env python
"""mapper.py"""
import json
import sys
from typing import Dict, List, Set

import pandas as pd
from pandas import DataFrame
from pandas.core.generic import NDFrame

pd.set_option("display.max_columns", None)


# pd.set_option('display.expand_frame_repr', False)


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


class HeaderChecker:
    __is_header: bool
    __correct_headers: Set[str]

    def __init__(self, set_headers: Set[str]):
        self.__is_header = True
        self.__correct_headers = set_headers

    @property
    def is_header(self) -> bool:
        return self.__is_header

    def is_not_ok(self, words: List[str]) -> bool:
        self.__is_header = False
        for header in self.__correct_headers:
            if header not in words:
                return True
        return False


class Mapper:
    __correct_headers: Set[str]
    __dico: Dict[str, any]

    def __init__(self, set_headers: Set[str]):
        self.__correct_headers = set_headers

    def filter(self, dataframe: DataFrame):
        filtered_dataframe = dataframe.filter(items=self.__correct_headers)
        self.__dico = filtered_dataframe.iloc[0].to_dict()
        return self

    def to_json(self) -> str:
        json_ligne = json.dumps(self.__dico)
        return json_ligne


headers = {
    "cpcli",
    "villecli",
    "codcde",
    "datcde"
    "codobj",
    "qte",
    "libobj",
    "points",
}

header_checker = HeaderChecker(headers)
mapper = Mapper(headers)
df: DataFrame = None

for line in sys.stdin:
    words = LineCleaner.delimit(line, ",")
    LineCleaner.clean_double_quote(words)
    if header_checker.is_header and header_checker.is_not_ok(words):
        df = DataFrame(columns=words)
        continue
    df.loc[0] = words  # inserer dans le df le tableau de data
    json_str = mapper.filter(df).to_json()
    print(json_str)
