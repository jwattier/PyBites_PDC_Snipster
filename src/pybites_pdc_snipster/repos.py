from abc import ABC, abstractmethod
from typing import Sequence

from sqlmodel import SQLModel

from pybites_pdc_snipster.exceptions import SnippetNotFoundError
from pybites_pdc_snipster.models import Snippet

SQLModel.__table_args__ = {"extend_existing": True}


class SnippetRepository(ABC):  # pragma: no cover
    @abstractmethod
    def add(self, snippet: Snippet) -> None:
        pass

    @abstractmethod
    def list(self) -> Sequence[Snippet]:
        pass

    @abstractmethod
    def get(self, snippet_id: int) -> Snippet | None:
        pass

    @abstractmethod
    def delete(self, snippet_id: int) -> None:
        pass


class InMemorySnippetRepot(SnippetRepository):
    def __init__(self) -> None:
        self._data: dict[int, Snippet] = {}

    def add(self, snippet: Snippet) -> None:
        next_id = max(self._data.keys(), default=0) + 1
        self._data[next_id] = snippet

    def list(self) -> list[Snippet]:
        return list(self._data.values())

    def get(self, snippet_id: int) -> Snippet | None:
        return self._data.get(snippet_id)

    def delete(self, snippet_id: int) -> None:
        if snippet_id not in self._data:
            raise SnippetNotFoundError(f"Snippet with id {snippet_id} not found")
        self._data.pop(snippet_id, None)


class DBSnippetRepot(SnippetRepository):
    pass


class JSONSnippetRepo(SnippetRepository):
    pass
