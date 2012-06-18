from django.conf.urls.defaults import *
from django.views.decorators.csrf import csrf_exempt

from checkin.conf import settings
from checkin.views import *

urlpatterns = patterns('',
    url(r'^checkin$',  csrf_exempt(CheckinSubmitView.as_view()), name='checkin-submit'),
)

#if settings.DEBUG:
urlpatterns = urlpatterns + patterns('',
    url(r'^map$',      CheckinMapView.as_view(),       name='checkin-map'),
    url(r'^console$',  CheckinConsoleView.as_view(),   name='checkin-console'),
)

