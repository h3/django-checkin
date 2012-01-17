from django.core.management.base import BaseCommand, CommandError

from checkin.models import Checkin

class Command(BaseCommand):
    args = ''
    help = 'Clear all checkins (non reversible !)'

    def handle(self, *args, **options):
        Checkin.objects.all().delete()
        self.stdout.write('Successfully removed all checkins.\n')


