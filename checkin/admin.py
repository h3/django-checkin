# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.admin import GeoModelAdmin

from checkin.models import *


class CheckinCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date_start', 'date_end', 'date_created', 'is_active')
admin.site.register(CheckinCampaign, CheckinCampaignAdmin)


class CheckinPlaceAdmin(GeoModelAdmin):
    list_display = ('name', 'campaign', 'lat', 'lon', 'point', 'date_created', 'is_active')
admin.site.register(CheckinPlace, CheckinPlaceAdmin)


class CheckinAdmin(GeoModelAdmin):
    list_display = ('place', 'lat', 'lon', 'accuracy', 'client_ip', 'success', 'date')
   #map_template = 'checkin/admin/openlayers.html'
admin.site.register(Checkin, CheckinAdmin)



