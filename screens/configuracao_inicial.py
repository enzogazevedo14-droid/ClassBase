from kivy.uix.screenmanager import Screen


ERROR_COLOR = (0.78, 0.20, 0.23, 1)


class InitialSetupScreen(Screen):
    def on_pre_enter(self, *args):
        if self.manager.auth_repository.count_users() > 0:
            self.manager.current = "login"

    def configure_account(self):
        username = self.ids.setup_username.text.strip()
        password = self.ids.setup_password.text
        confirm = self.ids.setup_confirm.text

        if password != confirm:
            self.ids.setup_feedback.color = ERROR_COLOR
            self.ids.setup_feedback.text = "As senhas não coincidem."
            return False

        try:
            self.manager.auth_repository.initialize_owner(username, password)
        except ValueError as exc:
            self.ids.setup_feedback.color = ERROR_COLOR
            self.ids.setup_feedback.text = str(exc)
            return False

        self.ids.setup_password.text = ""
        self.ids.setup_confirm.text = ""
        self.ids.setup_username.text = ""
        self.ids.setup_feedback.text = ""
        self.manager.get_screen("login").ids.username_input.text = username
        self.manager.current = "login"
        return True
