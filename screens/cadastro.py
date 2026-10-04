from kivy.uix.screenmanager import Screen


ERROR_COLOR = (0.78, 0.20, 0.23, 1)
SUCCESS_COLOR = (0.16, 0.56, 0.34, 1)

COURSES = (
    "Desenvolvimento de Sistemas",
    "Administração",
    "Recursos Humanos",
    "Outros",
)


class RegisterStudentScreen(Screen):
    def register_student(self):
        rm = self.ids.rm_input.text
        nome = self.ids.name_input.text
        curso = self.ids.course_input.text

        if curso == "Selecione o curso":
            curso = ""

        try:
            self.manager.repository.create_student(rm, nome, curso)
        except ValueError as exc:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = str(exc)
            return False

        self.ids.feedback.color = SUCCESS_COLOR
        self.ids.feedback.text = "Aluno cadastrado com sucesso."
        self.ids.rm_input.text = ""
        self.ids.name_input.text = ""
        self.ids.course_input.text = "Selecione o curso"
        return True
