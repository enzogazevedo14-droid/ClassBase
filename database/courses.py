import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database


class CourseRepository:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(self.db_path)

    @staticmethod
    def _clean_name(name):
        name = str(name).strip()
        if not name:
            raise ValueError("Nome do curso é obrigatório.")
        return name

    def create_course(self, name):
        name = self._clean_name(name)
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    "INSERT INTO cursos (nome, ativo) VALUES (?, 1)",
                    (name,),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um curso com este nome.") from exc

    def get_course(self, course_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT id, nome, ativo FROM cursos WHERE id = ?",
                (course_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_courses(self, include_inactive=False):
        with connect(self.db_path) as connection:
            if include_inactive:
                rows = connection.execute(
                    """
                    SELECT id, nome, ativo
                    FROM cursos
                    ORDER BY ativo DESC, nome COLLATE NOCASE, id
                    """
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, nome, ativo
                    FROM cursos
                    WHERE ativo = 1
                    ORDER BY nome COLLATE NOCASE, id
                    """
                ).fetchall()
        return [dict(row) for row in rows]

    def list_student_counts(self, include_inactive=True):
        condition = "" if include_inactive else "WHERE c.ativo = 1"

        with connect(self.db_path) as connection:
            rows = connection.execute(
                f"""
                SELECT
                    c.id,
                    c.nome,
                    c.ativo,
                    COUNT(a.id) AS total
                FROM cursos AS c
                LEFT JOIN alunos AS a ON a.curso_id = c.id
                {condition}
                GROUP BY c.id, c.nome, c.ativo
                ORDER BY total DESC, c.nome COLLATE NOCASE, c.id
                """
            ).fetchall()

        return [dict(row) for row in rows]

    def update_course(self, course_id, name):
        name = self._clean_name(name)
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    "UPDATE cursos SET nome = ? WHERE id = ?",
                    (name, course_id),
                )
                return cursor.rowcount == 1
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um curso com este nome.") from exc

    def set_course_active(self, course_id, active):
        with connect(self.db_path) as connection:
            cursor = connection.execute(
                "UPDATE cursos SET ativo = ? WHERE id = ?",
                (1 if active else 0, course_id),
            )
            return cursor.rowcount == 1

    def count_students(self, course_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS total FROM alunos WHERE curso_id = ?",
                (course_id,),
            ).fetchone()
        return row["total"]

    def delete_course(self, course_id):
        try:
            with connect(self.db_path) as connection:
                cursor = connection.execute(
                    "DELETE FROM cursos WHERE id = ?",
                    (course_id,),
                )
                return cursor.rowcount == 1
        except sqlite3.IntegrityError as exc:
            raise ValueError(
                "Não é possível excluir um curso vinculado a alunos."
            ) from exc
