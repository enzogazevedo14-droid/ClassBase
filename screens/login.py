from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text

        if self.manager.auth_repository.authenticate(username, password):
            self.ids.feedback.text = ""
            self.ids.password_input.text = ""
            if self.manager.auth_repository.requires_demo_password_change(username):
                change_screen = self.manager.get_screen("alterar_senha")
                change_screen.load_user(username)
                self.manager.current = "alterar_senha"
            else:
                self.manager.current = "home"
            return True

        self.ids.feedback.text = "Usuário ou senha inválidos."
        return False
