import sqlite3

from .connection import DEFAULT_DB_PATH, connect, initialize_database, utc_now


ORDER_BY = {
    "nome": "a.nome COLLATE NOCASE ASC, a.id ASC",
    "rm": "a.rm COLLATE NOCASE ASC, a.id ASC",
    "recentes": "a.created_at DESC, a.id DESC",
}


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
        timestamp = utc_now()

        try:
            with connect(self.db_path) as connection:
                course_id = self._find_active_course_id(connection, curso)
                cursor = connection.execute(
                    """
                    INSERT INTO alunos (
                        rm, nome, curso_id, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (rm, nome, course_id, timestamp, timestamp),
                )
                return cursor.lastrowid
        except sqlite3.IntegrityError as exc:
            raise ValueError("Já existe um aluno com este RM.") from exc

    def get_student(self, student_id):
        with connect(self.db_path) as connection:
            row = connection.execute(
                """
                SELECT
                    a.id,
                    a.rm,
                    a.nome,
                    a.curso_id,
                    c.nome AS curso,
                    a.created_at,
                    a.updated_at
                FROM alunos AS a
                JOIN cursos AS c ON c.id = a.curso_id
                WHERE a.id = ?
                """,
                (student_id,),
            ).fetchone()
        return dict(row) if row else None

    def list_students(self, search="", course="", order_by="nome"):
        term = str(search).strip()
        course = str(course).strip()
        order_clause = ORDER_BY.get(order_by, ORDER_BY["nome"])

        conditions = []
        params = []

        if term:
            pattern = f"%{term}%"
            conditions.append(
                "(a.rm LIKE ? OR a.nome LIKE ? OR c.nome LIKE ?)"
            )
            params.extend((pattern, pattern, pattern))

        if course:
            conditions.append("c.nome = ? COLLATE NOCASE")
            params.append(course)

        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)

        query = f"""
            SELECT
                a.id,
                a.rm,
                a.nome,
                a.curso_id,
                c.nome AS curso,
                a.created_at,
                a.updated_at
            FROM alunos AS a
            JOIN cursos AS c ON c.id = a.curso_id
            {where_clause}
            ORDER BY {order_clause}
        """

        with connect(self.db_path) as connection:
            rows = connection.execute(query, tuple(params)).fetchall()

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
                    SET rm = ?, nome = ?, curso_id = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        rm,
                        nome,
                        selected_course["id"],
                        utc_now(),
                        student_id,
                    ),
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
