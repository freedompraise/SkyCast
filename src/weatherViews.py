from django.views.generic import ListView
from .models import ClimateChange

class ClimateChangeView(ListView):
  model = ClimateChange
  template_name = 'climate_change.html'
  context_object_name = 'climate_change'

  def get_queryset(self):
    city_id = self.kwargs.get('city_id')
    return ClimateChange.objects.filter(city_id=city_id)

