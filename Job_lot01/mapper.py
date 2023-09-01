#!/usr/bin/env python
"""mapper.py"""

import sys
import pandas as pd
from classes.CSV_Cleaner import LineCleaner
from classes.CSV_HeaderCheck import AZE

header = {
    "cpcli",
    "villecli",
    "codcde",
    "datcde"
    "codobj",
    "qte",
    "libobj",
    "points",
}


aze = AZE()


for line in sys.stdin:
    if aze.is_first_line and aze.is_not_ok(line):
        continue
        
    words = LineCleaner.delimit(",")
    LineCleaner.clean_double_quote(words)

    print(words)
    dico = dict(words)

    json = pd.Series(dico).to_json()
    print(json)
