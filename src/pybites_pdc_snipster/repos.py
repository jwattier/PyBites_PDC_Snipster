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

    @abstractmethod
    def search(self, term: str, *, language: str | None = None) -> Sequence[Snippet]:
        pass

    @abstractmethod
    def toggle_favorite(self, snippet_id: int) -> None:
        pass

    @abstractmethod
    def tag(
        self, snippet_id: int, /, *tags: str, remove: bool = False, sort: bool = True
    ) -> None:
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

    def search(self, term: str, *, language: str | None = None) -> Sequence[Snippet]:
        pass

    def toggle_favorite(self, snippet_id: int) -> None:
        if snippet_id not in self._data:
            raise SnippetNotFoundError(f"Snippet with id {snippet_id} not found")

        if self._data[snippet_id].favorite is False:
            self._data[snippet_id].favorite = True
        else:
            self._data[snippet_id].favorite = False

    def tag(
        self, snippet_id: int, /, *tags: str, remove: bool = False, sort: bool = True
    ) -> None:
        pass


class DBSnippetRepot(AbstractSnippetRepository):
    def __init__(self, session: Session) -> None:
        # have the session exist at the instance/class level
        # that way the session management becomes easier across
        # multiple calls.
        self.session = session

    def add(self, snippet: Snippet) -> None:
        self.session.add(snippet)
        self.session.commit()
        self.session.refresh(snippet)

    def list(self) -> Sequence[Snippet]:
        stmt = select(Snippet)
        return list(self.session.exec(stmt).all())

    def get(self, snippet_id: int) -> Snippet | None:
        stmt = select(Snippet).where(Snippet.id == snippet_id)
        return self.session.exec(stmt).one_or_none()

    def delete(self, snippet_id: int) -> None:
        snippet_to_delete = self.session.get(Snippet, snippet_id)
        if snippet_to_delete is None:
            raise SnippetNotFoundError(f"Snippet with id {snippet_id} not found")
        self.session.delete(snippet_to_delete)
        self.session.commit()

    def search(self, term: str, *, language: str | None = None) -> Sequence[Snippet]:
        pass

    def toggle_favorite(self, snippet_id: int) -> None:
        stmt = select(Snippet).where(Snippet.id == snippet_id)
        results = self.session.exec(stmt).one_or_none()

        if results is not None:
            if results.favorite is True:
                results.favorite = False
            else:
                results.favorite = True

            self.session.add(results)
            self.session.commit()
            self.session.refresh(results)
        else:
            raise SnippetNotFoundError(f"Snippet with id {snippet_id} not found")

    def tag(
        self, snippet_id: int, /, *tags: str, remove: bool = False, sort: bool = True
    ) -> None:
        pass


class JSONSnippetRepo(AbstractSnippetRepository):
    pass
