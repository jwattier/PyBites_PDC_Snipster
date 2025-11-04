from abc import ABC, abstractmethod
from typing import Sequence

from sqlmodel import Session, select

from pybites_pdc_snipster.exceptions import SnippetNotFoundError
from pybites_pdc_snipster.models import Snippet


class AbstractSnippetRepository(ABC):  # pragma: no cover
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


class InMemorySnippetRepot(AbstractSnippetRepository):
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


class DBSnippetRepot(AbstractSnippetRepository):
    def __init__(self, session: Session) -> None:
        # have the session exist at the instance/class level
        # that way the session management becomes easier across
        # multiple calls.
        self.session = session

    def add(self, snippet: Snippet) -> dict:
        new_snippet = Snippet.create(**snippet.model_dump())
        self.session.add(new_snippet)
        self.session.commit()
        self.session.refresh(new_snippet)

        return new_snippet

    def list(self) -> list[Snippet] | None:
        stmt = select(Snippet)
        results = self.session.exec(stmt).all()

        return results if results else None

    def get(self, snippet_id: int) -> dict | None:
        stmt = select(Snippet).where(Snippet.snippet_id == snippet_id)
        snippet = self.session.exec(stmt).one_or_none()

        return snippet.model_dump() if snippet else None

    def delete(self, snippet_id: int) -> None:
        snippet_to_delete = self.session.get(Snippet, snippet_id)
        if snippet_to_delete is None:
            raise SnippetNotFoundError(f"Snippet with id {snippet_id} not found")

        self.session.delete(snippet_to_delete)
        self.session.commit()


class JSONSnippetRepo(AbstractSnippetRepository):
    pass
