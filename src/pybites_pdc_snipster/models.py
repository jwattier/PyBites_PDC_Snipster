from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine


class Snippet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    code: str
    description: str | None = None
    language: str  # TODO: Update the data type later to be int in conjunction with enumeration update
    tags: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime | None = None
    favorite: bool

    @classmethod
    def create(cls, **kwargs):
        snippet = cls(**kwargs)
        return snippet


# TODO create "add_snippet" function

if __name__ == "__main__":  # pragma: no cover
    sqlite_file_name = "snippet.db"
    sqllite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqllite_url, echo=False)
    SQLModel.metadata.create_all(engine)

    print("Database + table has been created.")
