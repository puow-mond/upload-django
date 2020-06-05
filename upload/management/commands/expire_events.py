from django.core.management.base import BaseCommand
from upload import tasks


class Command(BaseCommand):

    help = "Delete objects which are expired"

    def handle(self, *args, **options):
        tasks.delete_expired(repeat=60*5) # run tasks every 5 minutes
