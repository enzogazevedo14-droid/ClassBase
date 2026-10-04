from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


ERROR_COLOR = (0.78, 0.20, 0.23, 1)
SUCCESS_COLOR = (0.16, 0.56, 0.34, 1)


class EditStudentScreen(Screen):
    student_id = ObjectProperty(None, allownone=True)

    def load_student(self, student_id):
        student = self.manager.repository.get_student(student_id)
        if student is None:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Aluno não encontrado."
            return False

        self.student_id = student_id
        self.ids.rm_input.text = student["rm"]
        self.ids.name_input.text = student["nome"]
        self.ids.course_input.text = student["curso"]
        self.ids.feedback.text = ""
        return True

    def save_student(self):
        if self.student_id is None:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Nenhum aluno selecionado."
            return False

        curso = self.ids.course_input.text
        if curso == "Selecione o curso":
            curso = ""

        try:
            updated = self.manager.repository.update_student(
                self.student_id,
                self.ids.rm_input.text,
                self.ids.name_input.text,
                curso,
            )
        except ValueError as exc:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = str(exc)
            return False

        if not updated:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Aluno não encontrado."
            return False

        self.ids.feedback.color = SUCCESS_COLOR
        self.ids.feedback.text = "Aluno atualizado com sucesso."
        self.manager.current = "alunos"
        return True
