import datetime

from django.core.urlresolvers import reverse
from django import template

from checkin.models import CheckinPlace, Checkin

register = template.Library()


"""
Check if a used has checked in at a given place within a given amount of hours
"""

class CheckedInWithinLastNode(template.Node):
    def __init__(self, hours, place, user, varname, campaign=None):
        self.hours = float(hours)
        self.place = template.Variable(place)
        self.user = template.Variable(user)
        self.varname = varname
        if campaign:
            self.campaign = template.Variable(campaign)
        else:
            self.campaign = None
    
    def render(self, context):
        place_id = self.place.resolve(context).id
        qs = Checkin.objects.filter(place_id=place_id, user_id=self.user.resolve(context).id, is_valid=True,
                date__gte=(datetime.datetime.now() - datetime.timedelta(hours=self.hours)))
        if self.campaign:
            qs = qs.filter(place__campaign_id=self.campaign.resolve(context))
        context[self.varname] = qs.count() and qs[0] or False
        return ''

@register.tag()
def checked_in_within_last(parser, token):
    """
    {% checked_in_within_last 24 object request.user as has_checked_in 1 %}
    """
    bits = token.contents.split()
    if len(bits) != 6 and len(bits) != 7:
        raise template.TemplateSyntaxError, "checked_in_within_last tag takes 4 or 5 arguments"
    if bits[4] != 'as':
        raise template.TemplateSyntaxError, "second argument to the checked_in_within_last tag must be 'as'"
    if len(bits) == 6:
        return CheckedInWithinLastNode(bits[1], bits[2], bits[3], bits[5])
    else:
        return CheckedInWithinLastNode(bits[1], bits[2], bits[3], bits[5], bits[6])


"""
Get last checkin
"""

class GetLastCheckinNode(template.Node):
    def __init__(self, user, varname, hours=None):
        self.user = template.Variable(user)
        self.varname = varname
        if hours is not None:
            self.hours = float(hours)
    
    def render(self, context):
        user = self.user.resolve(context)
        if self.hours:
            qs = Checkin.objects.filter(user_id=user.id, is_valid=True,
                    date__gte=(datetime.datetime.now() - datetime.timedelta(hours=self.hours)))
        else:
            qs = Checkin.objects.filter(user_id=user.id, is_valid=True)
        context[self.varname] = qs.count() and qs[0] or False
        return ''

@register.tag()
def get_last_checkin(parser, token):
    """ 
    {% get_last_checkin user as last_checkin %}
    {% get_last_checkin user as last_checkin 24 %}
    """
    bits = token.contents.split()
    if len(bits) != 4 and len(bits) != 5:
        raise template.TemplateSyntaxError, "get_last_checkin tag takes 3 or 4 arguments"
    if bits[2] != 'as':
        raise template.TemplateSyntaxError, "second argument to the get_last_checkin tag must be 'as'"
    return GetLastCheckinNode(bits[1], bits[3], bits[4] or None)
