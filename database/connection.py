import sqlite3
from contextlib import contextmanager
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "classbase.db"


@contextmanager
def connect(db_path=DEFAULT_DB_PATH):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_database(db_path=DEFAULT_DB_PATH):
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rm TEXT NOT NULL UNIQUE,
                nome TEXT NOT NULL,
                curso TEXT NOT NULL
            )
            """
        )
