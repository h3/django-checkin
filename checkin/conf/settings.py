from django.conf import settings
from django.utils.translation import ugettext_lazy as _

DATABASE                = getattr(settings, 'CHECKIN_DATABASE', 'default')
DEBUG                   = getattr(settings, 'CHECKIN_DEBUG', False)
DEFAULT_PROXIMITY       = getattr(settings, 'CHECKIN_DEFAULT_PROXIMITY', 50)
DEFAULT_DISTANCE_UNIT   = getattr(settings, 'CHECKIN_DEFAULT_DISTANCE_UNIT', 'm')
DISTANCE_CHOICES        = getattr(settings, 'CHECKIN_DISTANCE_CHOICES', (
    ('m',  _('Meters')),
    ('km', _('Kilometers')),
    ('ft', _('Feet')),
    ('mi', _('Miles')),
))
