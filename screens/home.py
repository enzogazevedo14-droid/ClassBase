from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        if self.manager and self.manager.repository:
            total = self.manager.repository.count_students()
            self.ids.student_count.text = str(total)
