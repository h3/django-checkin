from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from checkin.models import *


class CheckinSubmitView(CreateView):
    model = Checkin

class CheckinMapView(ListView):
    model = Checkin
    template_name = 'checkin/map.html'
    def get_context_data(self, **kwargs):
        context = super(CheckinMapView, self).get_context_data(**kwargs)
        context['checkinplace_list'] = CheckinPlace.objects.all()
        return context


class CheckinConsoleView(TemplateView):
    template_name = 'checkin/console.html'
