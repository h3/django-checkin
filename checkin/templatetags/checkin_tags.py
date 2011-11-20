import datetime

from django.core.urlresolvers import reverse
from django import template

from checkin.models import CheckinPlace, Checkin

register = template.Library()

"""
Check if a used has checked in at a given place within a given amount of hours
"""

class CheckedInWithinLastNode(template.Node):
    def __init__(self, hours, place, user, varname):
        self.hours = float(hours)
        self.place = template.Variable(place)
        self.user = template.Variable(user)
        self.varname = varname
    
    def render(self, context):
        place_id = self.place.resolve(context).id
        qs = Checkin.objects.filter(place_id=place_id, user_id=self.user.resolve(context).id,
                date__gte=(datetime.datetime.now() - datetime.timedelta(hours=self.hours)))
        context[self.varname] = qs.count() and qs[0] or False
        return ''

@register.tag()
def checked_in_within_last(parser, token):
    bits = token.contents.split()
    if len(bits) != 6:
        raise template.TemplateSyntaxError, "checked_in_within_last tag takes exactly three arguments"
    if bits[4] != 'as':
        raise template.TemplateSyntaxError, "second argument to the checked_in_within_last tag must be 'as'"
    return CheckedInWithinLastNode(bits[1], bits[2], bits[3], bits[5])
