from django.apps import AppConfig


class KanbanAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kanban_app'

    def ready(self):
        import kanban_app.signals
