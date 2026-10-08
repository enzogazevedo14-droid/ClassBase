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

    @staticmethod
    def _find_course(connection, course_name):
        return connection.execute(
            """
            SELECT id, nome, ativo
            FROM cursos
            WHERE nome = ? COLLATE NOCASE
            """,
            (course_name,),
        ).fetchone()

    @classmethod
    def _find_active_course_id(cls, connection, course_name):
        course = cls._find_course(connection, course_name)
        if course is None or not course["ativo"]:
            raise ValueError("Curso não encontrado ou inativo.")
        return course["id"]

    def create_student(self, rm, nome, curso):
        rm, nome, curso = self._student_data(rm, nome, curso)
        try:
            with connect(self.db_path) as connection:
                course_id = self._find_active_course_id(connection, curso)
                cursor = connection.execute(
                    """
                    INSERT INTO alunos (rm, nome, curso_id)
                    VALUES (?, ?, ?)
                    """,
                    (rm, nome, course_id),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um aluno com este RM.") from exc

    def get_student(self, student_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT a.id, a.rm, a.nome, a.curso_id, c.nome AS curso
                FROM alunos AS a
                JOIN cursos AS c ON c.id = a.curso_id
                WHERE a.id = ?
                """,
                (student_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_students(self, search=""):
        term = str(search).strip()

        base_query = """
            SELECT a.id, a.rm, a.nome, a.curso_id, c.nome AS curso
            FROM alunos AS a
            JOIN cursos AS c ON c.id = a.curso_id
        """

        with connect(self.db_path) as connection:
            if term:
                pattern = f"%{term}%"
                rows = connection.execute(
                    base_query
                    + """
                    WHERE a.rm LIKE ?
                       OR a.nome LIKE ?
                       OR c.nome LIKE ?
                    ORDER BY a.nome COLLATE NOCASE, a.id
                    """,
                    (pattern, pattern, pattern),
                ).fetchall()
            else:
                rows = connection.execute(
                    base_query
                    + """
                    ORDER BY a.nome COLLATE NOCASE, a.id
                    """
                ).fetchall()
        return [dict(row) for row in rows]

    def update_student(self, student_id, rm, nome, curso):
        rm, nome, curso = self._student_data(rm, nome, curso)

        try:
            with connect(self.db_path) as connection:
                current = connection.execute(
                    "SELECT curso_id FROM alunos WHERE id = ?",
                    (student_id,),
                ).fetchone()

                if current is None:
                    return False

                selected_course = self._find_course(connection, curso)
                if selected_course is None:
                    raise ValueError("Curso não encontrado ou inativo.")

                if (
                    not selected_course["ativo"]
                    and selected_course["id"] != current["curso_id"]
                ):
                    raise ValueError("Curso não encontrado ou inativo.")

                cursor = connection.execute(
                    """
                    UPDATE alunos
                    SET rm = ?, nome = ?, curso_id = ?
                    WHERE id = ?
                    """,
                    (rm, nome, selected_course["id"], student_id),
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
