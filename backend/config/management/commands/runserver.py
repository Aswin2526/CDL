from django.contrib.staticfiles.management.commands.runserver import (
    Command as StaticfilesRunserverCommand,
)


class Command(StaticfilesRunserverCommand):
    """Development server with a clear startup success message."""

    def on_bind(self, server_port):
        super().on_bind(server_port)
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Backend is running successfully"))
