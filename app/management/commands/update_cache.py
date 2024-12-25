from django.core.management.base import BaseCommand
import app.utils

class Command(BaseCommand):
    help = 'update top users and tags'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        app.utils.updateCache()
