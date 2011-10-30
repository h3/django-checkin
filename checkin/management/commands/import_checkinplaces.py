import os, sys, commands

from django.utils import simplejson as json
from django.core.management.base import BaseCommand, CommandError

from checkin.models import CheckinPlace
from checkin.conf import settings


class Command(BaseCommand):
    args = ''
    help = 'Import checkin places'

    def handle(self, *args, **options):
        if len(args) == 0:
            print "Error: you must provide a file path to import."
            sys.exit()
        if not os.path.exists(args[0]):
            print "Error: file does not exists \"%s\"" % args[0]
            sys.exit()

        checkinplace = CheckinPlaceLoader(args[0], len(args) > 1 and int(args[1]) or 1)

        for data in checkinplace.next():
            cp = CheckinPlace(**data)
            cp.save()
            print "Inserted %(name)s - %(address)s (%(lng)s, %(lat)s)" % data
