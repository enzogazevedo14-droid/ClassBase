from kivy.uix.screenmanager import Screen


ERROR_COLOR = (0.78, 0.20, 0.23, 1)
SUCCESS_COLOR = (0.16, 0.56, 0.34, 1)
COURSE_PLACEHOLDER = "Selecione o curso"


class RegisterStudentScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh_courses()

    def refresh_courses(self):
        courses = self.manager.course_repository.list_courses()
        names = tuple(course["nome"] for course in courses)
        self.ids.course_input.values = names

        if self.ids.course_input.text not in names:
            self.ids.course_input.text = COURSE_PLACEHOLDER
        return names

    def register_student(self):
        rm = self.ids.rm_input.text
        nome = self.ids.name_input.text
        curso = self.ids.course_input.text

        if curso == COURSE_PLACEHOLDER:
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
        self.ids.course_input.text = COURSE_PLACEHOLDER
        return True
