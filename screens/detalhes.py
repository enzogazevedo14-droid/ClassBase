from datetime import datetime
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class StudentDetailScreen(Screen):
    student_id = ObjectProperty(None, allownone=True)

    @staticmethod
    def _format_timestamp(value):
        if not value:
            return "Não informado"

        try:
            moment = datetime.fromisoformat(value)
            return moment.astimezone().strftime("%d/%m/%Y %H:%M")
        except (TypeError, ValueError):
            return str(value)

    def load_student(self, student_id):
        student = self.manager.repository.get_student(student_id)
        if student is None:
            return False

        self.student_id = student_id
        self.ids.name_value.text = student["nome"]
        self.ids.rm_value.text = student["rm"]
        self.ids.course_value.text = student["curso"]
        self.ids.created_value.text = self._format_timestamp(student["created_at"])
        self.ids.updated_value.text = self._format_timestamp(student["updated_at"])
        return True

    def on_pre_enter(self, *args):
        if self.student_id is not None:
            self.load_student(self.student_id)

    def edit_student(self):
        if self.student_id is None:
            return False

        edit_screen = self.manager.get_screen("editar")
        if not edit_screen.load_student(self.student_id):
            return False

        self.manager.current = "editar"
        return True
