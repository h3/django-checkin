# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.admin import GeoModelAdmin, TabularInline

from checkin.models import *

if not settings.DEBUG:
    CHECKIN_READONLY_FIELDS = []
    CHECKIN_EXCLUDE_FIELDS = []
else:
    CHECKIN_EXCLUDE_FIELDS = ('lat', 'lng', 'place', 'user')
    CHECKIN_READONLY_FIELDS = (
            'get_place_display', 'get_latlon', 'get_campaign_display',
            'accuracy', 'visitor_ip', 'date', 'is_valid',
            'get_user_display', 'lng', 'lat', 'useragent', 'extra_data')


class CheckinCampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'proximity', 'min_accuracy', 'date_start', 'date_end', 'owner', 'date_created', 'is_active')
    list_editable = ('date_start', 'date_end')
    list_filter = ('owner', 'is_active')
    search_fields = ('name',)
    date_hierarchy = 'date_created'
admin.site.register(CheckinCampaign, CheckinCampaignAdmin)


class CheckinInline(TabularInline):
    fields = ('get_user_display', 'date', 'get_latlon', 'distance',  'accuracy', 'visitor_ip', 'useragent', 'is_valid')
    readonly_fields = ('date', 'get_latlon', 'distance', 'accuracy', 'visitor_ip', 'is_valid', 'useragent', 'get_user_display')
    exclude = ('extra_data', 'lat', 'lng')
    model = Checkin
    extra = 0
    
    def get_latlon(self, inst):
        return '<a href="http://maps.google.com/maps?q=%s%%20%s&z=17" target="_blank">%s / %s</a>' % (
                inst.lat, inst.lng, inst.lat, inst.lng)
    get_latlon.allow_tags = True
    get_latlon.short_description = _('Lat/Lon')

    def get_user_display(self, inst):
        url = reverse('admin:auth_user_change', args=(inst.id,))
        return '<a href="%s" target="_blank">%s</a>' % (url, unicode(inst.user))
    get_user_display.allow_tags = True
    get_user_display.short_description = _('User')



class CheckinPlaceAdmin(GeoModelAdmin):
    list_display = ('name', 'address', 'zipcode', 'city', 'campaign', 'get_proximity', 'get_min_accuracy', 'date_start', 'date_end', 'is_active')
    list_filter = ('campaign', 'campaign__owner', 'city', 'is_active',)
    list_editable = ('date_start', 'date_end')
    search_fields = ('name', 'address')
    date_hierarchy = 'date_created'
    exclude = ('distances_unit', )
    inlines = [CheckinInline]

    def get_proximity(self, obj):
        return obj.proximity or obj.campaign.proximity
    get_proximity.short_description = _('Proximity')

    def get_min_accuracy(self, obj):
        return obj.min_accuracy or obj.campaign.min_accuracy
    get_min_accuracy.short_description = _('Min. accuracy')

admin.site.register(CheckinPlace, CheckinPlaceAdmin)


class CheckinAdmin(GeoModelAdmin):
    list_display = ('date', 'user', 'get_place_display', 'get_campaign_display', 'get_latlon', 'accuracy', 'visitor_ip', 'is_valid')
    readonly_fields = CHECKIN_READONLY_FIELDS
    list_filter = ('place__name', 'place__campaign', 'is_valid',)
    search_fields = ('place__name', 'place__address')
    date_hierarchy = 'date'
    exclude = CHECKIN_EXCLUDE_FIELDS

    def get_place_display(self, inst):
        url = reverse('admin:checkin_checkinplace_change', args=(inst.place.id,))
        return '<a href="%s" target="_blank">%s</a>' % (url, unicode(inst.place))
    get_place_display.allow_tags = True
    get_place_display.short_description = _('Place')

    def get_campaign_display(self, inst):
        url = reverse('admin:checkin_checkincampaign_change', args=(inst.place.campaign.id,))
        return '<a href="%s" target="_blank">%s</a>' % (url, unicode(inst.place.campaign))
    get_campaign_display.allow_tags = True
    get_campaign_display.short_description = _('Campaign')

    def get_user_display(self, inst):
        url = reverse('admin:auth_user_change', args=(inst.id,))
        return '<a href="%s" target="_blank">%s</a>' % (url, unicode(inst.user))
    get_user_display.allow_tags = True
    get_user_display.short_description = _('User')

    def get_latlon(self, inst):
        return '<a href="http://maps.google.com/maps?q=%s%%20%s&z=17" target="_blank">%s / %s</a>' % (
                inst.lat, inst.lng, inst.lat, inst.lng)
    get_latlon.allow_tags = True
    get_latlon.short_description = _('Lat/Lon')

    def has_add_permission(self, request):
        if settings.DEBUG:
            return super(CheckinAdmin, self).has_add_permission(request)
        else:
            return False


   #map_template = 'checkin/admin/openlayers.html'
admin.site.register(Checkin, CheckinAdmin)



