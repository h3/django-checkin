Django-checkin
--------------

Dependencies
============

System packages
^^^^^^^^^^^^^^^
 * postgresql-9.1 
 * postgresql-contrib-9.1 
 * postgresql-server-dev-9.1
 * postgresql-9.1-postgis
 * binutils 
 * gdal-bin 
 * libproj-dev 
 # libxml2
 # libxml2-dev
 # libxslt1-dev 
 # libxslt1.1 
 # python-libxslt1 
 # python-libxml2

Python packages
^^^^^^^^^^^^^^^

 * django/geodjango (trunk or 1.4+)
 * django-tastypie (trunk)
 * pyproj
 * setuptools
 * psycopg2
 * django-tastypie
 * mimeparse >= 0.1.3
 * python-dateutil == 1.5
 * lxml
 * PyYAML
 * python_digest
 * biplist

Installation
============


settings.py
^^^^^^^^^^^

::

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
       #'django.contrib.gis',
        'django.contrib.admin',
       #'django.contrib.markup',

        'tastypie',
        'checkin',
    )


urls.py
^^^^^^^

::

    from django.conf.urls.defaults import *
    from django.contrib import admin

    from tastypie.api import Api
    from checkin.api import CheckinPlaceResource, CheckinResource

    v1_api = Api(api_name='v1')
    v1_api.register(CheckinPlaceResource())
    v1_api.register(CheckinResource())

    admin.autodiscover()

    urlpatterns = patterns('',
        (r'^admin/',     include(admin.site.urls)),
        (r'^api/',       include(v1_api.urls)),
    )
