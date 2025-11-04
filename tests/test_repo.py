import pytest
from sqlmodel import Session, SQLModel, create_engine

from pybites_pdc_snipster.exceptions import SnippetNotFoundError
from pybites_pdc_snipster.models import Snippet
from pybites_pdc_snipster.repos import DBSnippetRepot, InMemorySnippetRepot


def get_repo(name):
    if name == "memory":
        return InMemorySnippetRepot()
    elif name == "db":
        engine = create_engine("sqlite:///:memory:", echo=False)
        SQLModel.metadata.create_all(engine)
        with Session(engine) as session:
            return DBSnippetRepot(session=session)


# TODO: break up the test functions into memory tests and db tests
# currently the classes are structured differently enough that having separate tests makes
# more sense.
@pytest.fixture(scope="function", params=["memory", "db"])
def repo(request):
    return get_repo(request.param)


@pytest.fixture(scope="function")
def add_snippet(repo):
    snippet = Snippet(
        title="Hello World",
        code="print('Hello, World!')",
        description="A simple hello world snippet",
        language="python",
    )
    repo.add(snippet)
    return snippet


@pytest.fixture(scope="function")
def add_another_snippet(repo, add_snippet):
    another_snippet = Snippet(
        title="Hello World",
        code="print('Hello, World!')",
        description="A simple hello world snippet",
        language="rust",
    )
    repo.add(another_snippet)
    return another_snippet


def test_add_snippet(repo, add_snippet):
    assert repo._data[1] == add_snippet


def test_list_snippets_one_snippet(add_snippet, repo):
    assert len(repo.list()) == 1


def test_list_snippets_two_snippets(add_another_snippet, repo):
    assert len(repo.list()) == 2


def test_get_snippet(add_snippet, repo):
    assert repo.get(1) == add_snippet


def test_get_snippet_not_found(add_snippet, repo):
    assert repo.get(99999) is None


def test_delete_snippet(add_snippet, repo):
    repo.delete(1)
    assert repo._data.get(1) is None


def test_delete_non_existing_snippet(repo):
    with pytest.raises(SnippetNotFoundError):
        repo.delete(99999)
