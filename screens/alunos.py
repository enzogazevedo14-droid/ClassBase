from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class StudentListScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh_students()

    def refresh_students(self, search=None):
        if search is None:
            search = self.ids.search_input.text

        students = self.manager.repository.list_students(search)
        container = self.ids.student_list
        container.clear_widgets()

        if not students:
            container.add_widget(
                Label(
                    text="Nenhum aluno encontrado.",
                    size_hint_y=None,
                    height="56dp",
                )
            )
            return []

        for student in students:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height="76dp",
                spacing=8,
            )
            row.add_widget(
                Label(
                    text=(
                        f"{student['nome']}\n"
                        f"RM: {student['rm']} | {student['curso']}"
                    ),
                    halign="left",
                    valign="middle",
                )
            )

            edit_button = Button(text="Editar", size_hint_x=None, width="88dp")
            edit_button.bind(
                on_release=lambda _, sid=student["id"]: self.open_edit(sid)
            )
            row.add_widget(edit_button)

            delete_button = Button(text="Excluir", size_hint_x=None, width="88dp")
            delete_button.bind(
                on_release=lambda _, sid=student["id"], name=student["nome"]:
                    self.request_delete(sid, name)
            )
            row.add_widget(delete_button)
            container.add_widget(row)

        return students

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
