from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView, CreateView

from checkin.models import *


class CheckinSubmitView(CreateView):
    pass
#   def get_context_data(self, **kwargs):
#       context = super(HomeView, self).get_context_data(**kwargs)
#       #context['object_list'] = ...
#       return context

class CheckinMapView(ListView):
    template_name = 'checkin/map.html'


class CheckinConsoleView(TemplateView):
    template_name = 'checkin/console.html'
