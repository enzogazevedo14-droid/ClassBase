from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


ERROR_COLOR = (0.78, 0.20, 0.23, 1)


class ChangeDemoPasswordScreen(Screen):
    username = StringProperty("")

    def load_user(self, username):
        self.username = str(username).strip()
        self.ids.change_feedback.text = ""
        self.ids.current_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""

    def on_pre_enter(self, *args):
        if not self.username or not self.manager.auth_repository.requires_demo_password_change(
            self.username
        ):
            self.manager.current = "login"

    def update_password(self):
        if not self.username or not self.manager.auth_repository.requires_demo_password_change(
            self.username
        ):
            self.manager.current = "login"
            return False

        current = self.ids.current_password.text
        new = self.ids.new_password.text
        confirm = self.ids.confirm_password.text
        if new != confirm:
            self.ids.change_feedback.color = ERROR_COLOR
            self.ids.change_feedback.text = "As senhas não coincidem."
            return False

        try:
            changed = self.manager.auth_repository.change_password(
                self.username, current, new
            )
        except ValueError as exc:
            self.ids.change_feedback.color = ERROR_COLOR
            self.ids.change_feedback.text = str(exc)
            return False

        if not changed:
            self.ids.change_feedback.color = ERROR_COLOR
            self.ids.change_feedback.text = "Senha atual incorreta."
            return False

        self.ids.current_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""
        self.ids.change_feedback.text = ""
        self.manager.get_screen("login").ids.username_input.text = self.username
        self.username = ""
        # Exige novo login: não concede sessão autenticada automaticamente.
        self.manager.current = "login"
        return True

    def back_to_login(self):
        self.ids.current_password.text = ""
        self.ids.new_password.text = ""
        self.ids.confirm_password.text = ""
        self.username = ""
        self.manager.current = "login"
        return True
