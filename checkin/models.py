# -*- coding: utf-8 -*-

# vim: ai ts=4 sts=4 et sw=4
#from itertools import tee, izip

from datetime import datetime

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.measure import Distance as D
from django.contrib.gis.geos import *
from django.db.models import Q

from checkin.conf import settings

from itertools import chain


class CheckinManager(models.GeoManager):
    
    def nearby_places(self, lat=None, lng=None, accuracy=None, campaigns=None):
        out = []
        now = datetime.now()
        position = Point(lng, lat)

        for campaign in self.get_query_set().filter(
                Q(date_start__isnull=True) | Q(date_start__lte=now),
                Q(date_end__isnull=True) | Q(date_end__gte=now),
                pk__in=campaigns):
                
            rs = campaign.checkinplace_set.filter(
                    Q(date_start__isnull=True) | Q(date_start__lte=now),
                    Q(date_end__isnull=True) | Q(date_end__gte=now),
                    point__distance_lte=(position, D(m=campaign.proximity)),
                    is_active=True).distance(position).order_by('distance')

            if rs.count() > 0: out.append(rs)
        return list(chain(*out))

    def get_query_set(self):
        return super(CheckinManager, self).get_query_set()


class CheckinCampaign(models.Model):
    owner           = models.ForeignKey(User)
    name            = models.CharField(_('Name'), max_length=100)
    date_start      = models.DateTimeField(_('Date start'), blank=True, null=True)
    date_end        = models.DateTimeField(_('Date end'), blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
#   allow_multi_ci  = models.BooleanField(_('Allow overlaping checkins'), default=True)
    proximity       = models.IntegerField(_('Minimum required proximity'), default=settings.DEFAULT_PROXIMITY)
    min_accuracy    = models.IntegerField(_('Minimum required accuracy'), default=settings.DEFAULT_PROXIMITY)
    is_active       = models.BooleanField(_('Is active'), default=True)

    objects         = CheckinManager()

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

    def checkin(self, lng, lat, place_id=None):
        q = {'point__distance_lte': (Point(lng, lat), D(m=self.proximity)), 'is_active': True}
        if place_id:
            q['id'] = place_id
        
        qs = self.checkinplace_set.filter(**q)

        # TODO: second pass for checkin places that have custom proximity set
        if qs.count() > 0:
            # TODO: account for allow_multi_ci
            return qs
        else:
            return False

    def __unicode__(self):
        return u"%s" % self.name


class CheckinPlace(models.Model):
    campaign        = models.ForeignKey(CheckinCampaign)
    name            = models.CharField(_('Name'), max_length=100)
    address         = models.CharField(_('Address'), max_length=250, blank=True, null=True)
    city            = models.CharField(_('City'), max_length=100, blank=True, null=True)
    state           = models.CharField(_('State or province'), max_length=100, blank=True, null=True)
    zipcode         = models.CharField(_('Zip code'), max_length=10, blank=True, null=True)
    phone           = models.CharField(_('Phone'), max_length=15, blank=True, null=True)
    lng             = models.FloatField(_('Longitude'), blank=True, null=True)
    lat             = models.FloatField(_('Latitude'), blank=True, null=True)
    distances_unit  = models.CharField(_('Distance unit'), max_length=3, choices=settings.DISTANCE_CHOICES, default=settings.DEFAULT_DISTANCE_UNIT)
    proximity       = models.IntegerField(_('Minimum required proximity'), blank=True, null=True)
    min_accuracy    = models.IntegerField(_('Minimum required accuracy'), blank=True, null=True)
    date_start      = models.DateTimeField(_('Date start'), blank=True, null=True)
    date_end        = models.DateTimeField(_('Date end'), blank=True, null=True)
    date_created    = models.DateTimeField(_('Date created'), auto_now_add=True)
    is_active       = models.BooleanField(_('Is active'), default=True)

    point           = models.PointField(srid=4326, geography=True, blank=True, null=True)
    objects         = models.GeoManager()

    def save(self, *args, **kwargs):
        self.point = Point(self.lng, self.lat)
        super(CheckinPlace, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        unique_together = (("campaign", "lat", "lng"),)
        ordering = ("date_created", "name")


class Checkin(models.Model):
    date       = models.DateTimeField(_('Checkin date'), auto_now_add=True)
    place      = models.ForeignKey(CheckinPlace, blank=True, null=True)
    user       = models.ForeignKey(User)
    is_valid   = models.BooleanField(default=False)
    # Checkin infos
    lng        = models.FloatField()
    lat        = models.FloatField()
    accuracy   = models.FloatField(default=20000)
    timestamp  = models.DateTimeField(_('Checkin date'), auto_now_add=True)
    useragent  = models.CharField(max_length=250, default="Unknown")
    visitor_ip = models.IPAddressField(blank=True, null=True)
    extra_data = models.TextField(blank=True, null=True)

    def distance(self):
        try:
            place = CheckinPlace.objects.filter(pk=self.place.id).distance(Point(self.lng, self.lat))[0]
            if place.distance.m > 999: 
                return '~%0.3f km' % place.distance.km
            else:
                return '~%0.3f m' % place.distance.m
        except:
            return "Unknown"

    def __unicode__(self):
        title = self.is_valid and 'Valid checkin' or 'Invalid checkin'
        return u"%s at %s" % (title, self.place)

    class Meta:
        ordering = ('-date',)
