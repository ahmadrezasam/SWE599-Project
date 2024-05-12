from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.hello_world, name='test'),

    path('earthquakes/recent/', views.EarthquakesListView.as_view(), name='earthquackes'),
    path('earthquakes/', views.EarthquakesFilterListView.as_view(), name='earthquakes_filter'),
    path('earthquakes/date/', views.EarthquakesYearListView.as_view(), name='earthquakes_year'),
    path('earthquakes/list/', views.EarthquakesWithinAnArea.as_view(), name='earthquakes_list'),

    path('google_map_key/', views.GetGoogleMapAPIKey.as_view(), name='google_map_key'),

]