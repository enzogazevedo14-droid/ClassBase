from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text

        if self.manager.auth_repository.authenticate(username, password):
            self.ids.feedback.text = ""
            self.ids.password_input.text = ""
            self.manager.current = "home"
            return True

        self.ids.feedback.text = "Usuário ou senha inválidos."
        return False
