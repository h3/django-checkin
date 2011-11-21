# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.admin import GeoModelAdmin

from checkin.models import *


class CheckinCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date_start', 'date_end', 'date_created', 'is_active')
    list_editable = ('date_start', 'date_end')
    list_filter = ('owner', 'is_active')
    search_fields = ('name',)
    date_hierarchy = 'date_created'
admin.site.register(CheckinCampaign, CheckinCampaignAdmin)


class CheckinPlaceAdmin(GeoModelAdmin):
    list_display = ('name', 'address', 'campaign', 'date_start', 'date_end', 'is_active')
    list_filter = ('campaign', 'campaign__owner', 'is_active',)
    list_editable = ('date_start', 'date_end')
    search_fields = ('name', 'address')
    date_hierarchy = 'date_created'
admin.site.register(CheckinPlace, CheckinPlaceAdmin)


class CheckinAdmin(GeoModelAdmin):
    list_display = ('place', 'get_campaign', 'get_latlon', 'accuracy', 'visitor_ip', 'date', 'is_valid')
    list_filter = ('place__name', 'place__campaign', 'is_valid',)
    search_fields = ('place__name', 'place__address')
    date_hierarchy = 'date'

    def get_campaign(self, inst):
        return inst.place.campaign
    get_campaign.short_description = _('Campaign')

    def get_latlon(self, inst):
        return '<a href="http://maps.google.com/maps?q=%s%%20%s&z=17" target="_blank">%s / %s</a>' % (
                inst.lat, inst.lng, inst.lat, inst.lng)
    get_latlon.allow_tags = True
    get_latlon.short_description = _('Lat/Lon')


   #map_template = 'checkin/admin/openlayers.html'
admin.site.register(Checkin, CheckinAdmin)



