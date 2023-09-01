#!/usr/bin/env python
"""mapper.py"""

import sys
import pandas as pd
from pandas import DataFrame
sys.path.insert(0,"..")
from classes.CSV_Cleaner import LineCleaner
from classes.CSV_HeaderChecker import HeaderChecker
from classes.CSV_Mapper import Mapper


headers = {
    "cpcli",
    "villecli",
    "codcde",
    "timbrecde",
    "timbrecli",
    "points"
}

header_checker = HeaderChecker(headers)
mapper = Mapper(headers)
df: DataFrame = None

for line in sys.stdin:
    words = LineCleaner.delimit(line, ",")
    LineCleaner.clean_double_quote(words)
    if header_checker.is_header():
        if header_checker.is_not_correct(words):
            df = DataFrame(columns=words)
        continue
    df.loc[0] = words  # insert row in dataframe
    if not LineCleaner.has_clean_date(df):
        continue
    json_str = mapper.filter(df).to_json()
    print(json_str)
