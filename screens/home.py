from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        if self.manager and self.manager.repository:
            total = self.manager.repository.count_students()
            self.ids.student_count.text = str(total)

    def logout(self):
        login_screen = self.manager.get_screen("login")
        login_screen.ids.username_input.text = ""
        login_screen.ids.password_input.text = ""
        login_screen.ids.feedback.text = ""
        self.manager.current = "login"
        return True
