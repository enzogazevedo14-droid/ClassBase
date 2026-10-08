from datetime import datetime

from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


ENTITY_OPTIONS = {
    "Todos": "",
    "Alunos": "aluno",
    "Cursos": "curso",
}

ENTITY_LABELS = {
    "aluno": "Aluno",
    "curso": "Curso",
}


class HistoryScreen(Screen):
    @staticmethod
    def _format_timestamp(value):
        if not value:
            return "Data não informada"

        try:
            moment = datetime.fromisoformat(value)
            return moment.astimezone().strftime("%d/%m/%Y %H:%M")
        except (TypeError, ValueError):
            return str(value)

    def on_pre_enter(self, *args):
        self.refresh_history()

    def refresh_history(self):
        entity = ENTITY_OPTIONS.get(self.ids.entity_filter.text, "")
        events = self.manager.history_repository.list_events(entity=entity)

        self.ids.history_count.text = (
            "1 ação registrada"
            if len(events) == 1
            else f"{len(events)} ações registradas"
        )

        container = self.ids.history_list
        container.clear_widgets()

        if not events:
            container.add_widget(
                Label(
                    text="Nenhuma ação registrada.",
                    color=(0.40, 0.45, 0.52, 1),
                    size_hint_y=None,
                    height="64dp",
                )
            )
            return []

        for event in events:
            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height="140dp",
                padding=(12, 10),
                spacing=4,
            )

            with card.canvas.before:
                Color(1, 1, 1, 1)
                background = RoundedRectangle(
                    pos=card.pos,
                    size=card.size,
                    radius=[12],
                )

            card.bind(
                pos=lambda instance, value, shape=background: setattr(
                    shape, "pos", value
                ),
                size=lambda instance, value, shape=background: setattr(
                    shape, "size", value
                ),
            )

            entity_label = ENTITY_LABELS.get(
                event["entidade"],
                event["entidade"].title(),
            )
            title = Label(
                text=f"{entity_label} · {event['acao'].capitalize()}",
                color=(0.08, 0.27, 0.55, 1),
                bold=True,
                font_size="14sp",
                halign="left",
                valign="middle",
                size_hint_y=None,
                height="28dp",
            )
            title.bind(
                size=lambda instance, value: setattr(
                    instance, "text_size", value
                )
            )
            card.add_widget(title)

            description = Label(
                text=event["descricao"],
                color=(0.10, 0.14, 0.20, 1),
                font_size="13sp",
                halign="left",
                valign="middle",
                size_hint_y=None,
                height="72dp",
            )
            description.bind(
                size=lambda instance, value: setattr(
                    instance, "text_size", value
                )
            )
            card.add_widget(description)

            date_label = Label(
                text=self._format_timestamp(event["created_at"]),
                color=(0.42, 0.47, 0.55, 1),
                font_size="12sp",
                halign="left",
                valign="middle",
                size_hint_y=None,
                height="24dp",
            )
            date_label.bind(
                size=lambda instance, value: setattr(
                    instance, "text_size", value
                )
            )
            card.add_widget(date_label)
            container.add_widget(card)

        return events
