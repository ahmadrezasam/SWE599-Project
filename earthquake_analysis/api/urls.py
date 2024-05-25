from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from . import views

urlpatterns = [
    path('test/', views.hello_world, name='test'),

    path('earthquakes/recent/', views.EarthquakesListView.as_view(), name='earthquackes'),
    path('earthquakes/', views.EarthquakesFilterListView.as_view(), name='earthquakes_filter'),
    path('earthquakes/date/', views.EarthquakesYearListView.as_view(), name='earthquakes_year'),
    path('earthquakes/list/within_area/', views.EarthquakesWithinAnArea.as_view(), name='earthquakes_list'),

    path('google_map_key/', views.GetGoogleMapAPIKey.as_view(), name='google_map_key'),

    path('docs/', include_docs_urls(title='Earthquake API', description='API for all things earthquakes')),
    path(
        "schema/",
        get_schema_view(
            title="Earthquake API", description="API for all earthquakes", version="1.0.0"
        ),
        name="openapi-schema",
    ),
]