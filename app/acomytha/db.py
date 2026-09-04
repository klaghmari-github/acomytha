"""Session SQLAlchemy 2.0."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.orm import Session, sessionmaker

from acomytha.models import Base
from acomytha.settings import Settings


class Database:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine = create_engine(
            settings.database_url,
            connect_args={"check_same_thread": False},
            future=True,
        )

        @event.listens_for(self._engine, "connect")
        def _sqlite_pragmas(dbapi_conn, _rec) -> None:  # noqa: ANN001
            cur = dbapi_conn.cursor()
            cur.execute("PRAGMA foreign_keys=ON")
            cur.execute("PRAGMA journal_mode=WAL")
            cur.close()

        self._session_factory = sessionmaker(bind=self._engine, autoflush=False, autocommit=False, future=True)

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def engine(self):
        return self._engine

    @property
    def SessionLocal(self):
        return self._session_factory

    def create_all(self) -> None:
        Base.metadata.create_all(self.engine)
        self._migrate()

    def _migrate(self) -> None:
        insp = inspect(self.engine)
        if "stories" not in insp.get_table_names():
            return
        cols = {c["name"] for c in insp.get_columns("stories")}
        if "duration_s" not in cols:
            with self.engine.begin() as conn:
                conn.execute(text("ALTER TABLE stories ADD COLUMN duration_s INTEGER DEFAULT 0"))
        if "has_interaction" not in cols:
            with self.engine.begin() as conn:
                conn.execute(text("ALTER TABLE stories ADD COLUMN has_interaction BOOLEAN DEFAULT 0"))

    def session(self) -> Generator[Session, None, None]:
        db = self._session_factory()
        try:
            yield db
        finally:
            db.close()
