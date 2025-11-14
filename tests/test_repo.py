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
    repo.add(add_snippet)
    if hasattr(repo, "_data"):
        assert repo._data[1] == add_snippet
    else:
        result = repo.get(1)
        assert result is not None
        assert result.title == add_snippet.title
        assert result.language == add_snippet.language


@pytest.fixture
def example_snippet() -> Snippet:
    return Snippet(title="Test", code="print('hi')", language="python")


@pytest.fixture
def example_snippets() -> list[Snippet]:
    return [
        Snippet(
            title="print to stdout",
            code="print('hello world')",
            language="python",
        ),
        Snippet(
            title="get user input",
            code="input('enter name: ')",
            language="python",
        ),
        Snippet(
            title="random number",
            code="let _ = nums.choose(&mt rng);",
            language="rust",
        ),
    ]


@pytest.fixture
def add_snippets(repo, example_snippets):
    for snippet in example_snippets:
        repo.add(snippet)


def test_list_snippets_one_snippet(add_snippet, repo):
    assert len(repo.list()) == 1


def test_list_snippets_two_snippets(add_another_snippet, repo):
    assert len(repo.list()) == 2


def test_get_snippet(add_snippet, repo):
    repo.add(add_snippet)
    assert repo.get(1) == add_snippet


def test_get_snippet_not_found(add_snippet, repo):
    assert repo.get(99999) is None


def test_delete_snippet(add_snippet, repo):
    repo.add(add_snippet)
    repo.delete(1)
    if hasattr(repo, "_data"):
        assert repo._data.get(1) is None
    else:
        assert repo.get(1) is None


def test_delete_non_existing_snippet(repo):
    with pytest.raises(SnippetNotFoundError):
        repo.delete(99999)


def test_favorite_snippet(repo, add_snippets):
    snippet = repo.get(1)
    assert snippet.favorite is False
    repo.toggle_favorite(1)
    snippet = repo.get(1)
    assert snippet.favorite is True
    repo.toggle_favorite(1)
    snippet = repo.get(1)
    assert snippet.favorite is False
    with pytest.raises(SnippetNotFoundError):
        repo.toggle_favorite(100)


def test_tag_snippet(repo, add_snippets):
    pass


def test_search_snippet(repo, add_snippets):
    pass
