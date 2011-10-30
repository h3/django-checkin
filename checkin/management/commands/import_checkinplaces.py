import os, sys, commands

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

from checkin.models import CheckinPlace
from checkin.conf import settings



class ConnectionLoader(object):
    def __init__(self, l):
        if isinstance(l, basestring):
            try:
                module_name, klass_name = l.rsplit('.', 1)
                module = import_module(module_name)
            except ImportError, e:
                raise ImproperlyConfigured('Error importing database loader %s: "%s"' % (klass_name, e))
            try:
                loader_class = getattr(module, klass_name)
            except AttributeError:
                raise ImproperlyConfigured('Module "%s" does not define a database loader name "%s"' % (module, klass_name))
            else:
                self.loader = loader_class
        else:
            self.loader = l

    def init(self, path, campaign_id=1):
        self.inst = self.loader(path, campaign_id)
        self.next = self.inst.next



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
        print settings.PLACE_LOADER
        loader = ConnectionLoader(settings.PLACE_LOADER)

        loader.init(args[0], len(args) > 1 and int(args[1]) or 1)
        print loader

        for data in loader.next():
            cp = CheckinPlace(**data)
            cp.save()
            print "Inserted %(name)s - %(address)s (%(lng)s, %(lat)s)" % data
