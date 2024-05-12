import django_filters
from .models import Earthquake

class EarthquakeFilter(django_filters.FilterSet):
    class Meta:
        model = Earthquake
        fields = {
            'latitude': ['exact', 'lt', 'gt'], 
            'longitude': ['exact', 'lt', 'gt'], 
            'depth': ['exact', 'lt', 'gt'],
            'magnitude': ['exact', 'lt', 'gt'],
            'date': ['exact', 'lt', 'gt'],
        }
