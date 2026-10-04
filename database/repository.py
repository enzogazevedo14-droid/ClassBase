import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database


class StudentRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(self.db_path)

    @staticmethod
    def _clean(value, field_name):
        value = str(value).strip()
        if not value:
            raise ValueError(f"{field_name} é obrigatório.")
        return value

    @classmethod
    def _student_data(cls, rm, nome, curso):
        return (
            cls._clean(rm, "RM"),
            cls._clean(nome, "Nome"),
            cls._clean(curso, "Curso"),
        )

    def create_student(self, rm, nome, curso):
        rm, nome, curso = self._student_data(rm, nome, curso)
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    "INSERT INTO alunos (rm, nome, curso) VALUES (?, ?, ?)",
                    (rm, nome, curso),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um aluno com este RM.") from exc

    def get_student(self, student_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT id, rm, nome, curso FROM alunos WHERE id = ?",
                (student_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_students(self, search=""):
        term = str(search).strip()
        with connect(self.db_path) as connection:
            if term:
                pattern = f"%{term}%"
                rows = connection.execute(
                    """
                    SELECT id, rm, nome, curso
                    FROM alunos
                    WHERE rm LIKE ? OR nome LIKE ? OR curso LIKE ?
                    ORDER BY nome COLLATE NOCASE, id
                    """,
                    (pattern, pattern, pattern),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, rm, nome, curso
                    FROM alunos
                    ORDER BY nome COLLATE NOCASE, id
                    """
                ).fetchall()
        return [dict(row) for row in rows]

    def update_student(self, student_id, rm, nome, curso):
        rm, nome, curso = self._student_data(rm, nome, curso)
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    """
                    UPDATE alunos
                    SET rm = ?, nome = ?, curso = ?
                    WHERE id = ?
                    """,
                    (rm, nome, curso, student_id),
                )
                return cursor.rowcount == 1
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um aluno com este RM.") from exc

    def delete_student(self, student_id):
        with connect(self.db_path) as connection:
            cursor = connection.execute(
                "DELETE FROM alunos WHERE id = ?",
                (student_id,),
            )
            return cursor.rowcount == 1

    def count_students(self):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM alunos"
            ).fetchone()
        return row["total"]
