# -*- coding: utf-8 -*-

# vim: ai ts=4 sts=4 et sw=4
#from itertools import tee, izip

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.measure import Distance as D
from django.contrib.gis.geos import *


DISTANCE_UNIT_CHOICES = (
    ('m',  _('Meters')),
    ('km', _('Kilometers')),
    ('ft', _('Feet')),
    ('mi', _('Miles')),
    #'nm', _('Nautical')),
)


class CheckinCampaign(models.Model):
    owner           = models.ForeignKey(User)
    name            = models.CharField(max_length=100)
    distances_unit  = models.CharField(max_length=3, choices=DISTANCE_UNIT_CHOICES, default="m")
    proximity       = models.IntegerField(default=10)
    date_start      = models.DateTimeField(_('Date start'), blank=True, null=True)
    date_end        = models.DateTimeField(_('Date end'), blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
    allow_multi_ci  = models.BooleanField(_('Allow overlaping checkins'), default=True)
    is_active       = models.BooleanField(_('Is active'), default=True)

    def _format_distance(self, pnt):
        self.distances_unit
        if self.distances_unit == 'km':
            return (pnt, D(km=self.proximity))
        elif self.distances_unit == 'mi':
            return (pnt, D(mi=self.proximity))
        elif self.distances_unit == 'ft':
            return (pnt, D(ft=self.proximity))
        else:
            return (pnt, D(m=self.proximity))

    def checkin(self, lon, lat):
        qs = self.checkinplace_set.filter(point__distance_lte=self._format_distance(Point(lon, lat)))
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
    name            = models.CharField(max_length=100)
    campaign        = models.ForeignKey(CheckinCampaign)
    address         = models.CharField(max_length=250, blank=True, null=True)
    lon             = models.FloatField(blank=True, null=True)
    lat             = models.FloatField(blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
    is_active       = models.BooleanField(_('Is active'), default=True)

    point           = models.PointField(srid=4326, geography=True, blank=True, null=True)
    objects         = models.GeoManager()

    def save(self, *args, **kwargs):
        self.point = Point(self.lon, self.lat)
        super(CheckinPlace, self).save(*args, **kwargs)

    def __repr__(self):
        return "<CheckinPlace('%s','%s')>" % (self.name, self.point)

    def __unicode__(self):
        if self.name:
            return u"%s at lat: %s, lon: %s" % (self.name, self.lat, self.lon)
        else:
            return u"Untitled place at lat: %s, lon: %s" % (self.lat, self.lon)



class CheckinLog(models.Model):
    lon        = models.FloatField()
    lat        = models.FloatField()
    date       = models.DateTimeField(_('Checkin date'), auto_now_add=True)
    place      = models.ForeignKey(CheckinPlace, blank=True, null=True)
    useragent  = models.CharField(max_length=250, default="Unknown")
    accuracy   = models.IntegerField(default=20000)
    client_ip  = models.IPAddressField(blank=True, null=True)
    visitor_ip = models.IPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)
    success    = models.BooleanField(default=False)

    def __repr__(self):
        return "<CheckinLog('%s','%s','%s','%s','%s')>" % (
            self.place, self.lat, self.lon, self.client_ip, self.date)
