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

Python packages
^^^^^^^^^^^^^^^

 * django/geodjango (trunk or 1.4+)
 * pyproj
 * setuptools
 * psycopg2

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
        'django.contrib.admin',

        'django.contrib.gis',
        'checkin',
    )


urls.py
^^^^^^^

::

    from django.conf.urls.defaults import *
    from django.contrib import admin

    admin.autodiscover()

    urlpatterns = patterns('',
        (r'^admin/',    include(admin.site.urls)),
        (r'^checkin/',  include('checkin.urls')),
    )
