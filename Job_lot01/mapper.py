#!/usr/bin/env python
"""mapper.py"""
import json
import sys
from typing import Dict, List, Set

import pandas as pd
from pandas import DataFrame
from pandas.core.generic import NDFrame

sys.path.insert(0, "..")

from classes.CSV_Cleaner import LineCleaner
from classes.CSV_HeaderChecker import HeaderChecker
from classes.CSV_Mapper import Mapper

pd.set_option("display.max_columns", None)

# pd.set_option('display.expand_frame_repr', False)


headers = {
    "cpcli",
    "villecli",
    "codcde",
    "datcde",
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
    if header_checker.is_header():
        if header_checker.is_not_correct(words):
            break
        df = DataFrame(columns=words)
        continue
    df.loc[0] = words  # insert row in dataframe
    if not LineCleaner.has_clean_date(df):
        continue
    json_str = mapper.filter(df).to_json()
    print(json_str)
