from typing import List, Set


class HeaderChecker:
    __is_first_line: True
    __correct_headers: Set[str]

    def __init__(self, set_headers: Set[str]):
        self.__correct_headers = set_headers

    @property
    def is_header(self) -> bool:
        return self.__is_first_line

    def is_not_ok(self, words: List[str]) -> bool:
        self.__is_first_line = False
        for header in self.__correct_headers:
            if header not in words:
                return True
        return False
