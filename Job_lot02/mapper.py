#!/usr/bin/env python
"""mapper.py"""
import json
import sys
from typing import Set, Any, List

import numpy as np
import pandas as pd
from dateutil.parser import parse
from pandas import DataFrame


class Mapper:

    def __init__(self, set_headers: Set[str]):
        self.__correct_headers = set_headers
        self.__dico = {}

    def filter(self, dataframe: DataFrame):
        filtered_dataframe = dataframe.filter(items=self.__correct_headers)
        self.__dico = filtered_dataframe.iloc[0].to_dict()
        return self

    def to_json(self) -> str:
        json_ligne = json.dumps(self.__dico,default=convert_int64_to_int)
        return json_ligne

    def to_raw_str(self) -> str:
        valeurs = []
        for valeur in self.__dico.values():
            valeurs.append(valeur)
        resultat = ', '.join(valeurs)
        return resultat

class HeaderChecker:

    def __init__(self, set_headers: Set[str]):
        self.__is_header = True
        self.__correct_headers = set_headers

    def is_header(self) -> bool:
        return self.__is_header

    def is_not_correct(self, words_array: List[str]) -> bool:
        self.__is_header = False
        for header in self.__correct_headers:
            if header not in words_array:
                return True
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
        date = pd.to_datetime(dataframe['datcde'],errors='coerce').dt.year
        try:
            date = int(date)
            if date >= startYear and date <= endYear:
                return True
            return False
        except:
            return False

def is_valid_date(value: Any):
    try:
        parse(str(value), fuzzy=True, dayfirst=True)
        return True
    except ValueError:
        return False

def convert_int64_to_int(obj):
    if isinstance(obj, np.int64):
        return int(obj)
    return obj

headers = {
    "cpcli",
    "villecli",
    "codcde",
    "timbrecde",
    "timbrecli",
    "points",
    "datcde"
}

header_checker = HeaderChecker(headers)
mapper = Mapper(headers)
df = None
# counter = 0

for line in sys.stdin:
    # counter += 1
    # if counter>20000:
    #     break
    words = LineCleaner.delimit(line, ",")
    LineCleaner.clean_double_quote_if_not_empty(words)
    if header_checker.is_header():
        if header_checker.is_not_correct(words):
            break
        df = DataFrame(columns=words)
        continue
    try:
        df.loc[0] = words  # insert row in dataframe
    except:
        continue
    if not LineCleaner.has_clean_date(df):
        continue
    if not LineCleaner.is_between_years(df,2006,2016):
        continue
    df['points'] = pd.to_numeric(df['points'], errors='coerce', downcast='integer')
    df['points'] = df['points'].apply(lambda x: max(x, 0))
    json_str = mapper.filter(df).to_json()
    print(json_str)
