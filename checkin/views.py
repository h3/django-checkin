from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView
from django.views.generic.edit import ProcessFormView
from django.utils import simplejson

from checkin.models import *


class CheckinMapView(TemplateView):
    template_name = 'checkin/map.html'
    def get_context_data(self, **kwargs):
        context = super(CheckinMapView, self).get_context_data(**kwargs)
        context['checkinplace_list'] = CheckinPlace.objects.all()
        return context

#from webcore.utils.debug import brake

class CheckinSubmitView(ProcessFormView):
    
    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden(u"Nice try. I'll tell your mom about this.")

    def post(self, request, *args, **kwargs):
        print request.POST
       #brake()()
        obj         = Checkin()
        campaign    = get_object_or_404(CheckinCampaign, pk=request.POST['cid'])
        checkin     = campaign.checkin(float(request.POST['coords[longitude]']), float(request.POST['coords[latitude]']))
        if checkin:
            obj.is_valid = True
            obj.place_id = checkin[0].id # TODO: support multiple checkins
            place = {
                'id': checkin[0].id,
                'name': checkin[0].name,
                'address': checkin[0].address,
            }
        else:
            obj.is_valid = False
            place = False

        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
            real_ip = real_ip.split(",")[0]
        except KeyError:
            real_ip = request.META['REMOTE_ADDR']

        obj.lng        = request.POST['coords[longitude]']
        obj.lat        = request.POST['coords[latitude]']
        obj.accuracy   = request.POST['coords[accuracy]']
        obj.timestamp  = request.POST['timestamp']
        obj.useragent  = request.POST['useragent']
        obj.visitor_ip = real_ip
#       obj.extra_data = 
        obj.save()
            
        return HttpResponse(simplejson.dumps({
            'errors': False,
            'checkin': {
                'place': place,
                'is_valid': obj.is_valid,
                'lng': obj.lng,
                'lat': obj.lat,
                'accuracy': obj.accuracy,
                'timestamp': obj.timestamp,
            }
            
        }), mimetype='application/json')
 

class CheckinConsoleView(TemplateView):
    template_name = 'checkin/console.html'
