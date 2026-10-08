from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput


ERROR_COLOR = (0.78, 0.20, 0.23, 1)
SUCCESS_COLOR = (0.16, 0.56, 0.34, 1)


class CourseScreen(Screen):
    def on_pre_enter(self, *args):
        self.refresh_courses()

    def create_course(self):
        name = self.ids.course_name_input.text
        try:
            self.manager.course_repository.create_course(name)
        except ValueError as exc:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = str(exc)
            return False

        self.ids.course_name_input.text = ""
        self.ids.feedback.color = SUCCESS_COLOR
        self.ids.feedback.text = "Curso cadastrado com sucesso."
        self.refresh_courses()
        self._refresh_student_course_choices()
        return True

    def refresh_courses(self):
        courses = self.manager.course_repository.list_courses(include_inactive=True)
        container = self.ids.course_list
        container.clear_widgets()
        self.ids.course_count.text = f"{len(courses)} curso(s) cadastrado(s)"

        for course in courses:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height="118dp",
                padding=(12, 10),
                spacing=8,
            )
            with card.canvas.before:
                Color(1, 1, 1, 1)
                background = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[12],
                )
            card.bind(
                pos=lambda instance, value, shape=background: setattr(shape, "pos", value),
                size=lambda instance, value, shape=background: setattr(shape, "size", value),
            )

            status = "Ativo" if course["ativo"] else "Inativo"
            info = Label(
                text=f"{course['nome']}\nStatus: {status}",
                color=(0.10, 0.14, 0.20, 1),
                font_size="14sp",
                halign="left",
                valign="middle",
                size_hint_y=None,
                height="52dp",
            )
            info.bind(size=lambda instance, value: setattr(instance, "text_size", value))
            card.add_widget(info)

            actions = BoxLayout(size_hint_y=None, height="40dp", spacing=6)

            edit_button = Button(
                text="Editar",
                background_normal="",
                background_color=(0.90, 0.94, 1, 1),
                color=(0.08, 0.27, 0.55, 1),
            )
            edit_button.bind(
                on_release=lambda _, cid=course["id"]: self.open_edit(cid)
            )
            actions.add_widget(edit_button)

            toggle_button = Button(
                text="Desativar" if course["ativo"] else "Ativar",
                background_normal="",
                background_color=(0.91, 0.94, 0.99, 1),
                color=(0.09, 0.28, 0.58, 1),
            )
            toggle_button.bind(
                on_release=lambda _, cid=course["id"], active=course["ativo"]:
                    self.toggle_course(cid, active)
            )
            actions.add_widget(toggle_button)

            delete_button = Button(
                text="Excluir",
                background_normal="",
                background_color=(0.88, 0.25, 0.28, 1),
                color=(1, 1, 1, 1),
            )
            delete_button.bind(
                on_release=lambda _, cid=course["id"], name=course["nome"]:
                    self.request_delete(cid, name)
            )
            actions.add_widget(delete_button)

            card.add_widget(actions)
            container.add_widget(card)

        return courses

    def open_edit(self, course_id):
        course = self.manager.course_repository.get_course(course_id)
        if course is None:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Curso não encontrado."
            return False

        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        name_input = TextInput(
            text=course["nome"],
            multiline=False,
            size_hint_y=None,
            height="48dp",
        )
        popup_feedback = Label(
            text="",
            color=ERROR_COLOR,
            size_hint_y=None,
            height="34dp",
        )
        content.add_widget(name_input)
        content.add_widget(popup_feedback)

        actions = BoxLayout(size_hint_y=None, height="48dp", spacing=8)
        cancel_button = Button(text="Cancelar")
        save_button = Button(text="Salvar")
        actions.add_widget(cancel_button)
        actions.add_widget(save_button)
        content.add_widget(actions)

        popup = Popup(
            title="Editar curso",
            content=content,
            size_hint=(0.88, None),
            height=dp(260),
            auto_dismiss=False,
        )
        cancel_button.bind(on_release=popup.dismiss)

        def save_course(*_):
            try:
                updated = self.manager.course_repository.update_course(
                    course_id,
                    name_input.text,
                )
            except ValueError as exc:
                popup_feedback.text = str(exc)
                return

            if not updated:
                popup_feedback.text = "Curso não encontrado."
                return

            popup.dismiss()
            self.ids.feedback.color = SUCCESS_COLOR
            self.ids.feedback.text = "Curso atualizado com sucesso."
            self.refresh_courses()
            self._refresh_student_course_choices()

        save_button.bind(on_release=save_course)
        popup.open()
        return True

    def toggle_course(self, course_id, currently_active):
        updated = self.manager.course_repository.set_course_active(
            course_id,
            not bool(currently_active),
        )
        if not updated:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Curso não encontrado."
            return False

        action = "ativado" if not currently_active else "desativado"
        self.ids.feedback.color = SUCCESS_COLOR
        self.ids.feedback.text = f"Curso {action} com sucesso."
        self.refresh_courses()
        self._refresh_student_course_choices()
        return True

    def request_delete(self, course_id, course_name):
        content = BoxLayout(orientation="vertical", padding=16, spacing=12)
        content.add_widget(
            Label(text=f"Deseja excluir o curso {course_name}?")
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
            size_hint=(0.88, 0.35),
            auto_dismiss=False,
        )
        cancel_button.bind(on_release=popup.dismiss)

        def confirm_delete(*_):
            popup.dismiss()
            self.delete_course(course_id)

        delete_button.bind(on_release=confirm_delete)
        popup.open()

    def delete_course(self, course_id):
        try:
            deleted = self.manager.course_repository.delete_course(course_id)
        except ValueError as exc:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = str(exc)
            return False

        if not deleted:
            self.ids.feedback.color = ERROR_COLOR
            self.ids.feedback.text = "Curso não encontrado."
            return False

        self.ids.feedback.color = SUCCESS_COLOR
        self.ids.feedback.text = "Curso excluído com sucesso."
        self.refresh_courses()
        self._refresh_student_course_choices()
        return True

    def _refresh_student_course_choices(self):
        for screen_name in ("cadastro", "editar"):
            if self.manager.has_screen(screen_name):
                screen = self.manager.get_screen(screen_name)
                if hasattr(screen, "refresh_courses"):
                    screen.refresh_courses()
