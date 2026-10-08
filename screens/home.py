from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        if not self.manager or not self.manager.repository:
            return

        total = self.manager.repository.count_students()
        self.ids.student_count.text = str(total)

        counts = self.manager.course_repository.list_student_counts(
            include_inactive=False
        )
        populated = [course for course in counts if course["total"] > 0]

        if not populated:
            self.ids.course_summary.text = "Nenhum aluno distribuído por curso."
            return

        visible = populated[:4]
        lines = [
            f"{course['nome']}: {course['total']}"
            for course in visible
        ]

        if len(populated) > len(visible):
            lines.append(f"+ {len(populated) - len(visible)} outro(s) curso(s)")

        self.ids.course_summary.text = "\n".join(lines)

    def logout(self):
        login_screen = self.manager.get_screen("login")
        login_screen.ids.username_input.text = ""
        login_screen.ids.password_input.text = ""
        login_screen.ids.feedback.text = ""
        self.manager.current = "login"
        return True
