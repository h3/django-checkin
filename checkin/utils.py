# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
from django.contrib.auth.models import User

from checkin.models import Checkin


def get_last_checkin_for_user(user, campaign=None):
    """
    Returns the last checkin for a given user.
    
    >>> from django.contrib.auth.models import User
    >>> usr = User.objects.all()[0]
    >>> get_last_checkin_for_user(usr)
    >>> None
    """
    try:
        return Checkin.objects.order_by('-date').filter(user_id=user.id, is_valid=True)[0]
    except:
        return None


