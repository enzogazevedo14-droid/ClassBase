from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


ALL_COURSES = "Todos os cursos"
ORDER_OPTIONS = {
    "Nome A-Z": "nome",
    "RM": "rm",
    "Mais recentes": "recentes",
}


class StudentListScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh_filters()
        self.refresh_students()

    def refresh_filters(self):
        courses = self.manager.course_repository.list_courses(include_inactive=True)
        values = (ALL_COURSES,) + tuple(course["nome"] for course in courses)
        self.ids.course_filter.values = values

        if self.ids.course_filter.text not in values:
            self.ids.course_filter.text = ALL_COURSES

        return values

    def refresh_students(self, search=None):
        if search is None:
            search = self.ids.search_input.text

        selected_course = self.ids.course_filter.text
        course = "" if selected_course == ALL_COURSES else selected_course
        order_by = ORDER_OPTIONS.get(self.ids.order_filter.text, "nome")

        students = self.manager.repository.list_students(
            search=search,
            course=course,
            order_by=order_by,
        )

        total = len(students)
        self.ids.result_count.text = (
            "1 aluno encontrado"
            if total == 1
            else f"{total} alunos encontrados"
        )

        container = self.ids.student_list
        container.clear_widgets()

        if not students:
            container.add_widget(
                Label(
                    text="Nenhum aluno encontrado.",
                    color=(0.40, 0.45, 0.52, 1),
                    size_hint_y=None,
                    height="64dp",
                )
            )
            return []

        for student in students:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="136dp",
                spacing=10,
                padding=(12, 8),
            )
            with row.canvas.before:
                Color(1, 1, 1, 1)
                background = RoundedRectangle(
                    pos=row.pos,
                    size=row.size,
                    radius=[12],
                )
            row.bind(
                pos=lambda instance, value, shape=background: setattr(shape, "pos", value),
                size=lambda instance, value, shape=background: setattr(shape, "size", value),
            )

            student_label = Label(
                text=(
                    f"{student['nome']}\n"
                    f"RM: {student['rm']}\n"
                    f"{student['curso']}"
                ),
                color=(0.10, 0.14, 0.20, 1),
                font_size="14sp",
                halign="left",
                valign="middle",
            )
            student_label.bind(
                size=lambda instance, value: setattr(instance, "text_size", value)
            )
            row.add_widget(student_label)

            actions = BoxLayout(
                orientation="vertical",
                size_hint_x=None,
                width="86dp",
                spacing=5,
            )

            details_button = Button(
                text="Detalhes",
                font_size="13sp",
                background_normal="",
                background_color=(0.90, 0.94, 1, 1),
                color=(0.08, 0.27, 0.55, 1),
            )
            details_button.bind(
                on_release=lambda _, sid=student["id"]: self.open_detail(sid)
            )
            actions.add_widget(details_button)

            edit_button = Button(
                text="Editar",
                font_size="13sp",
                background_normal="",
                background_color=(0.90, 0.94, 1, 1),
                color=(0.08, 0.27, 0.55, 1),
            )
            edit_button.bind(
                on_release=lambda _, sid=student["id"]: self.open_edit(sid)
            )
            actions.add_widget(edit_button)

            delete_button = Button(
                text="Excluir",
                font_size="13sp",
                background_normal="",
                background_color=(0.88, 0.25, 0.28, 1),
                color=(1, 1, 1, 1),
            )
            delete_button.bind(
                on_release=lambda _, sid=student["id"], name=student["nome"]:
                    self.request_delete(sid, name)
            )
            actions.add_widget(delete_button)

            row.add_widget(actions)
            container.add_widget(row)

        return students

    def open_detail(self, student_id):
        detail_screen = self.manager.get_screen("detalhes")
        if not detail_screen.load_student(student_id):
            return False

        self.manager.current = "detalhes"
        return True

    def open_edit(self, student_id):
        edit_screen = self.manager.get_screen("editar")
        if not edit_screen.load_student(student_id):
            return False

        self.manager.current = "editar"
        return True

    def request_delete(self, student_id, student_name):
        content = BoxLayout(orientation="vertical", padding=16, spacing=12)
        content.add_widget(
            Label(text=f"Deseja excluir {student_name}?")
        )

        actions = BoxLayout(size_hint_y=None, height="48dp", spacing=8)
        cancel_button = Button(text="Cancelar")
        delete_button = Button(text="Excluir")
        actions.add_widget(cancel_button)
        actions.add_widget(delete_button)
        content.add_widget(actions)

        popup = Popup(
            title="Confirmar exclusão",
            content=content,
            size_hint=(0.85, 0.35),
            auto_dismiss=False,
        )
        cancel_button.bind(on_release=popup.dismiss)

        def confirm_delete(*_):
            self.delete_student(student_id)
            popup.dismiss()

        delete_button.bind(on_release=confirm_delete)
        popup.open()

    def delete_student(self, student_id):
        deleted = self.manager.repository.delete_student(student_id)
        self.refresh_students()
        return deleted
