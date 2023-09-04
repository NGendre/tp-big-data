import json
from typing import Dict, Set

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
        json_ligne = json.dumps(self.__dico)
        return json_ligne

    def to_raw_str(self) -> str:
        valeurs = []
        for valeur in self.__dico.values():
            valeurs.append(valeur)
        resultat = ', '.join(valeurs)
        return resultat
