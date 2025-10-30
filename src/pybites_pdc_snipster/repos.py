from abc import ABC, abstractmethod
from typing import Sequence

from sqlmodel import Session, SQLModel, select

from pybites_pdc_snipster.exceptions import SnippetNotFoundError
from pybites_pdc_snipster.models import Snippet


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
    def __init__(self):
        self._data: dict[int, Snippet] = {}

    def add(self, snippet: Snippet, engine) -> None:
        with Session(engine) as session:
            session.add(snippet)
            session.commit()

    def list():
        pass

    def get(self, snippet_id: int, engine) -> Snippet | None:
        pass
        # with Session(engine) as session:

    def delete(self, snippet: Snippet, snippet_id: int, engine) -> None:
        # TODO: does the scenario of if the snippet id is not in the class need to be handled?
        # I don't believe a value not being in the database creates an error with the select

        with Session(engine) as session:
            statement = select(snippet).where(snippet.id == snippet_id)
            results = session.exec(statement)
            deleted_snippet = results.one()
            print(f"Snippet: {deleted_snippet} will be deleted.")

            session.delete(deleted_snippet)
            session.commit()


class JSONSnippetRepo(SnippetRepository):
    pass
