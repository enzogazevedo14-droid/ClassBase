import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "classbase.db"
DEFAULT_COURSES = (
    "Desenvolvimento de Sistemas",
    "Administração",
    "Recursos Humanos",
    "Outros",
)
SCHEMA_VERSION = 3


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


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


def _table_columns(connection, table_name):
    return {
        row["name"]
        for row in connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    }


def _create_courses_table(connection):
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE COLLATE NOCASE,
            ativo INTEGER NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1))
        )
        """
    )

    for course_name in DEFAULT_COURSES:
        connection.execute(
            "INSERT OR IGNORE INTO cursos (nome, ativo) VALUES (?, 1)",
            (course_name,),
        )


def _create_students_table(connection, table_name="alunos"):
    connection.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rm TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            curso_id INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        )
        """
    )


def _migrate_legacy_students(connection, columns):
    old_courses = connection.execute(
        """
        SELECT DISTINCT TRIM(curso) AS nome
        FROM alunos
        WHERE TRIM(curso) <> ''
        """
    ).fetchall()

    for row in old_courses:
        connection.execute(
            "INSERT OR IGNORE INTO cursos (nome, ativo) VALUES (?, 1)",
            (row["nome"],),
        )

    migrated_at = utc_now()
    connection.execute("DROP TABLE IF EXISTS alunos_latest")
    _create_students_table(connection, "alunos_latest")

    connection.execute(
        """
        INSERT INTO alunos_latest (
            id, rm, nome, curso_id, created_at, updated_at
        )
        SELECT a.id, a.rm, a.nome, c.id, ?, ?
        FROM alunos AS a
        JOIN cursos AS c
          ON c.nome = TRIM(a.curso) COLLATE NOCASE
        """,
        (migrated_at, migrated_at),
    )

    connection.execute("DROP TABLE alunos")
    connection.execute("ALTER TABLE alunos_latest RENAME TO alunos")


def _migrate_relational_students_with_timestamps(connection, columns):
    migrated_at = utc_now()
    connection.execute("DROP TABLE IF EXISTS alunos_latest")
    _create_students_table(connection, "alunos_latest")

    created_expression = "a.created_at" if "created_at" in columns else "?"
    updated_expression = "a.updated_at" if "updated_at" in columns else "?"

    params = []
    if "created_at" not in columns:
        params.append(migrated_at)
    if "updated_at" not in columns:
        params.append(migrated_at)

    connection.execute(
        f"""
        INSERT INTO alunos_latest (
            id, rm, nome, curso_id, created_at, updated_at
        )
        SELECT
            a.id,
            a.rm,
            a.nome,
            a.curso_id,
            {created_expression},
            {updated_expression}
        FROM alunos AS a
        """,
        tuple(params),
    )

    connection.execute("DROP TABLE alunos")
    connection.execute("ALTER TABLE alunos_latest RENAME TO alunos")


def _migrate_students_to_latest(connection):
    columns = _table_columns(connection, "alunos")

    if not columns:
        _create_students_table(connection)
        return

    if "curso" in columns and "curso_id" not in columns:
        _migrate_legacy_students(connection, columns)
        return

    if "curso_id" not in columns:
        raise RuntimeError("Schema de alunos incompatível com a migração do ClassBase.")

    if "created_at" not in columns or "updated_at" not in columns:
        _migrate_relational_students_with_timestamps(connection, columns)


def initialize_database(db_path=DEFAULT_DB_PATH):
    with connect(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                salt BLOB NOT NULL,
                senha_hash BLOB NOT NULL
            )
            """
        )

        _create_courses_table(connection)
        _migrate_students_to_latest(connection)
        connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
