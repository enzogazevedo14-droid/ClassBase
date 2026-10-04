from kivy.app import App
from kivy.uix.label import Label


class ClassBaseApp(App):
    def build(self):
        self.title = "ClassBase"
        return Label(text="ClassBase\nAmbiente configurado com sucesso")


if __name__ == "__main__":
    ClassBaseApp().run()
