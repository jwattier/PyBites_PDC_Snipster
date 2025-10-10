from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    code: str
    description: str | None = None
    language: int  # enumeration
    tags: str | None = None
    created_at: datetime = Field(default_factory=datetime.now(datetime.timezone.utc))
    updated_at: datetime | None = None
    favorite: bool


sqlite_file_name = "snippet_db.db"
sqllite_url = f"sqlite://{sqlite_file_name}"

engine = create_engine(sqllite_url, echo=False)

SQLModel.metadata.create_all(engine)
