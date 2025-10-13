import pytest
from sqlmodel import Session, SQLModel, create_engine

from src.pybites_pdc_snipster.models import Snippet

engine = create_engine("sqlite:///memory", echo=True)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)


def test_create_snippet():
    snippet = Snippet(
        title="Test Snippet",
        code="print(Hello, World!)",
        description="Just a test snippet, nothing more, nothing less",
        language="Python",
        tags="['test', 'example']",
        favorite=False,
    )
    with Session(engine) as session:
        session.add(snippet)
        session.commit()
        session.refresh(snippet)  # get the id on the object

    assert snippet.id is not None
    assert snippet.title == "Test Snippet"
    assert snippet.code == "print(Hello, World!)"
    assert snippet.language == "Python"


def test_create_snippet_with_cls_method():
    snippet_dict = {
        "title": "Test Snippet",
        "code": "print(Hello, World!)",
        "description": "Just a test snippet, nothing more, nothing less",
        "language": "Python",
        "tags": "['test', 'example']",
        "favorite": False,
    }
    snippet = Snippet.create(**snippet_dict)

    with Session(engine) as session:
        session.add(snippet)
        session.commit()
        session.refresh(snippet)  # get the id on the object

    assert snippet.id is not None
    assert snippet.title == "Test Snippet"
    assert snippet.code == "print(Hello, World!)"
    assert snippet.language == "Python"
