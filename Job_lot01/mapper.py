#!/usr/bin/python
"""mapper.py"""
import json
import sys
from typing import List, Set

import numpy as np

sys.path.insert(0, "..")

from pandas import DataFrame
from dateutil.parser import parse


def is_valid_date(value):
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
            if word != "" and word[0] == '"' and word[-1] == '"':
                word = word[1:]
                word = word[:-1]
                words[index] = word

    @staticmethod
    def has_clean_date(dataframe: DataFrame) -> bool:
        valid_date = dataframe['datcde'].apply(is_valid_date)
        return valid_date.bool()


class HeaderChecker:

    def __init__(self, set_headers: Set[str]):
        self.__is_header = True
        self.__correct_headers = set_headers

    def is_header(self) -> bool:
        return self.__is_header

    def is_not_correct(self, words_array: List[str]) -> bool:
        self.__is_header = False
        # print(words_array)
        for header in self.__correct_headers:
            if header not in words_array:
                # print(header, "not in")
                return True
        return False


def convert_int64_to_int(obj):
    if isinstance(obj, np.int64):
        return int(obj)
    return obj


class Mapper:

    def __init__(self, set_headers: Set[str]):
        self.__correct_headers = set_headers
        self.__dico = {}

    def filter(self, dataframe: DataFrame):
        filtered_dataframe = dataframe.filter(items=self.__correct_headers)
        self.__dico = filtered_dataframe.iloc[0].to_dict()
        return self

    def to_json(self) -> str:
        json_ligne = json.dumps(self.__dico, default=convert_int64_to_int)
        return json_ligne

    def to_raw_str(self) -> str:
        valeurs = []
        for valeur in self.__dico.values():
            valeurs.append(valeur)
        resultat = ', '.join(valeurs)
        return resultat


headers = {
    "cpcli",
    "villecli",
    "codcde",
    "datcde",
    "codobj",
    "qte",
    "libobj",
    "points",
    "codcli",
    "Colis"
}

header_checker = HeaderChecker(headers)
mapper = Mapper(headers)
df = None
count = 0
for line in sys.stdin:
    if line == "":
        break
    words = LineCleaner.delimit(line, ",")
    LineCleaner.clean_double_quote(words)
    if header_checker.is_header():
        if header_checker.is_not_correct(words):
            break
        df = DataFrame(columns=words)

        continue
    try:
        df.loc[0] = words  # insert row in dataframe
        df = df.astype({'qte': int, 'points': int, 'Colis': int})
    except:
        continue
    if not LineCleaner.has_clean_date(df):
        continue

    json_str = mapper.filter(df).to_json()
    print(json_str)
