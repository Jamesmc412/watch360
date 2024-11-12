from django.apps import AppConfig


class WatchappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watchapp'  # Ensure this matches your app's folder name

class WatchappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'watchapp'

    def ready(self):
        import watchapp.signals  # Import signals when the app is ready