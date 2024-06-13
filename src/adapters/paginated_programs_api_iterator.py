
from typing import Optional
import requests
from core.ports.programs_iterator import ProgramsIterator, ProgramsIteratorBuilder

class ProgramsPaginatedAPIIteratorBuilder(ProgramsIteratorBuilder):
    def __init__(self, base_url: str, limit:Optional[int]=None):
        self._base_url = base_url
        self._limit = limit

    def build(self) -> ProgramsIterator:
        return ProgramsPaginatedAPIIterator(self._base_url, self._limit)


class ProgramsPaginatedAPIIterator(ProgramsIterator):
    def __init__(self, base_url: str, limit:Optional[int]=None):
        self.base_url = base_url
        self.limit = limit
        self.current_page_index = 0
        self.current_page_data = []
        self.current_page_data_index = 0
        self.total_index = 0
        self._fetch_page()

    def _fetch_page(self):
        self.current_page_index += 1
        response = requests.get(
            self.base_url, 
            params={
                "page": self.current_page_index, 
                "resultsPerPage": 10
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        # TODO We should do some checks on data type here.
        self.current_page_data = data['items']
        self.total_pages = data['pagination']['nb_pages']
        self.current_page_data_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.limit and self.total_index >= self.limit:
            raise StopIteration

        if self.current_page_data_index >= len(self.current_page_data):
            if self.current_page_index <= self.total_pages:
                self._fetch_page()
                return self.__next__()
            raise StopIteration

        result = self.current_page_data[self.current_page_data_index]
        self.current_page_data_index += 1
        self.total_index += 1
        return result