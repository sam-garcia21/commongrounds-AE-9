from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from localevents.models import Event

# Create your views here.
class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'


class EventDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'