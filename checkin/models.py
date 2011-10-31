# -*- coding: utf-8 -*-

# vim: ai ts=4 sts=4 et sw=4
#from itertools import tee, izip

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.measure import Distance as D
from django.contrib.gis.geos import *

from checkin.conf import settings


class CheckinCampaign(models.Model):
    owner           = models.ForeignKey(User)
    name            = models.CharField(_('Name'), max_length=100)
    date_start      = models.DateTimeField(_('Date start'), blank=True, null=True)
    date_end        = models.DateTimeField(_('Date end'), blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
    allow_multi_ci  = models.BooleanField(_('Allow overlaping checkins'), default=True)
    proximity       = models.IntegerField(_('Minimum required proximity'), default=settings.DEFAULT_PROXIMITY)
    min_accuracy    = models.IntegerField(_('Minimum required accuracy'), default=settings.DEFAULT_PROXIMITY)
    is_active       = models.BooleanField(_('Is active'), default=True)

   #def _format_distance(self, pnt):
   #   #return (pnt, D(**{self.distances_unit: self.proximity}))
   #    if self.distances_unit == 'km':
   #        return (pnt, D(km=self.proximity))
   #    elif self.distances_unit == 'mi':
   #        return (pnt, D(mi=self.proximity))
   #    elif self.distances_unit == 'ft':
   #        return (pnt, D(ft=self.proximity))
   #    else:
   #        return (pnt, D(m=self.proximity))

    def checkin(self, lng, lat):
        qs = self.checkinplace_set.filter(point__distance_lte=(Point(lng, lat), D(m=self.proximity)))
        # TODO: second pass for checkin places that have custom proximity set
        if qs.count() > 0:
            # TODO: account for allow_multi_ci
            print "Sucessful checkin !!"
            return qs
        else:
            return False

    def __repr__(self):
        return "<CheckinCampaign('%s','%s','%s','%s')>" % (
            self.name, self.owner, self.date_start, self.date_end)

    def __unicode__(self):
        return u"%s" % self.name


class CheckinPlace(models.Model):
    campaign        = models.ForeignKey(CheckinCampaign)
    name            = models.CharField(_('Name'), max_length=100)
    address         = models.CharField(_('Address'), max_length=250, blank=True, null=True)
    lng             = models.FloatField(_('Longitude'), blank=True, null=True)
    lat             = models.FloatField(_('Latitude'), blank=True, null=True)
    distances_unit  = models.CharField(_('Distance unit'), max_length=3, choices=settings.DISTANCE_CHOICES, default=settings.DEFAULT_DISTANCE_UNIT)
    proximity       = models.IntegerField(_('Minimum required proximity'), blank=True, null=True)
    min_accuracy    = models.IntegerField(_('Minimum required accuracy'), blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
    is_active       = models.BooleanField(_('Is active'), default=True)

    point           = models.PointField(srid=4326, geography=True, blank=True, null=True)
    objects         = models.GeoManager()

    def save(self, *args, **kwargs):
        self.point = Point(self.lng, self.lat)
        super(CheckinPlace, self).save(*args, **kwargs)

    def __repr__(self):
        return "<CheckinPlace('%s','%s')>" % (self.name, self.point)

    def __unicode__(self):
        return u"%s at lat: %s, lng: %s (%s)" % (self.name, self.lat, self.lng, self.campaign)

    class Meta:
        unique_together = (("campaign", "lat", "lng"),)
        ordering = ("date_created", "name")


class Checkin(models.Model):
    date       = models.DateTimeField(_('Checkin date'), auto_now_add=True)
    place      = models.ForeignKey(CheckinPlace, blank=True, null=True)
    is_valid   = models.BooleanField(default=False)
    # Checkin infos
    lng        = models.FloatField()
    lat        = models.FloatField()
    accuracy   = models.IntegerField(default=20000)
    timestamp  = models.DateTimeField(_('Checkin date'), auto_now_add=True)
    useragent  = models.CharField(max_length=250, default="Unknown")
    visitor_ip = models.IPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)

    def __repr__(self):
        return "<CheckinLog('%s','%s','%s','%s','%s')>" % (
            self.place, self.lat, self.lng, self.client_ip, self.date)

    def __unicode__(self):
        title = self.is_valid and 'Valid checkin' or 'Invalid checkin'
        return u"%s at %s" % (title, self.place)
