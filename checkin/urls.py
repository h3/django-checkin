from django.conf.urls.defaults import *

from checkin.conf import settings
from checkin.views import *

urlpatterns = patterns('',
    url(r'^(?P<lat>\f)/(?P<lng>\f)/(?P<cid>\w+)/$',      
        CheckinSubmitView.as_view(), name='checkin-submit'),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + patterns('',
    url(r'^map/$',      CheckinMapView.as_view(),       name='checkin-map'),
    url(r'^console/$',  CheckinConsoleView.as_view(),   name='checkin-console'),
)

