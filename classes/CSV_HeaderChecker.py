from typing import List, Set


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
