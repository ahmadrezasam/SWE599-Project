from django.shortcuts import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


from .models import Earthquake
from .serializers import EarthquakesSerializer
from .filters import EarthquakeFilter

from django.conf import settings
from django.http import QueryDict


from django.db.models import Q

import math

# Create your views here.
def hello_world(requst):
    return HttpResponse("Hello world!")

class EarthquakesListView(APIView):
    def get(self, request):
        earthquakes = Earthquake.objects.order_by('-event_id')[:50]
        serializer = EarthquakesSerializer(earthquakes, many=True)
        return Response(serializer.data)
    
class EarthquakesFilterListView(APIView):
    def get(self, request):

        filtered_query_params = QueryDict(mutable=True)
        print("request.query_params: ", request.query_params)

        for key, value in request.query_params.items():
            if value:
                filtered_query_params.appendlist(key, value)
        
        for field_name, value in filtered_query_params.items():
            if f'{field_name}__lt' in filtered_query_params or f'{field_name}__gt' in filtered_query_params:
                return Response({"Error": f"Cannot use 'lt' or 'gt' filters along with '{field_name}'"}, status=status.HTTP_400_BAD_REQUEST)
        
        queryset = Earthquake.objects.all()
        filter_set = EarthquakeFilter(filtered_query_params, queryset=queryset)
        filtered_queryset = filter_set.qs[:200]
        serializer = EarthquakesSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    
class EarthquakesYearListView(APIView):
    def get(self, request):

        year = request.query_params.get('year')
        month = request.query_params.get('month')
        day = request.query_params.get('day')

        earthquakes = Earthquake.objects.all()

        if year is not None:
            earthquakes = earthquakes.filter(date__year=year)
        if month is not None:
            earthquakes = earthquakes.filter(date__month=month)
        if day is not None:
            earthquakes = earthquakes.filter(date__day=day)

        serializer = EarthquakesSerializer(earthquakes, many=True)
        return Response(serializer.data)

def check(marker, circle, radius):  
        km = radius / 1000
        kx = math.cos(math.pi * circle['lat'] / 180) * 111
        dx = abs(circle['lng'] - marker['lng']) * kx
        dy = abs(circle['lat'] - marker['lat']) * 111
        return math.sqrt(dx * dx + dy * dy) <= km
class EarthquakesWithinAnArea(APIView):
    def get(self, request):

        circle_center_lat_str = request.GET.get('circle_center_lat')
        circle_center_lng_str = request.GET.get('circle_center_lng')
        circle_radius_str = request.GET.get('circle_radius')

        filtered_query_params = QueryDict(mutable=True)
        for key, value in request.query_params.items():
            if value:
                filtered_query_params.appendlist(key, value)
        
        for field_name, value in filtered_query_params.items():
            if f'{field_name}__lt' in filtered_query_params or f'{field_name}__gt' in filtered_query_params:
                return Response({"Error": f"Cannot use 'lt' or 'gt' filters along with '{field_name}'"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not all([circle_center_lat_str, circle_center_lng_str, circle_radius_str]):
            return Response({'error': 'circle_center_lat, circle_center_lng, and circle_radius are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            circle_center_lat = float(circle_center_lat_str)
            circle_center_lng = float(circle_center_lng_str)
            circle_radius = float(circle_radius_str)
        except ValueError:
            return Response({'error': 'Invalid parameter value. Please provide valid numbers for circle_center_lat, circle_center_lng, and circle_radius.'}, status=status.HTTP_400_BAD_REQUEST)

        circle = {'lat': circle_center_lat, 'lng': circle_center_lng}

        queryset = Earthquake.objects.all()
        earthquakes_within_area = []
        for earthquake in queryset:
            marker = {'lat': earthquake.latitude, 'lng': earthquake.longitude}
            if check(marker, circle, circle_radius):
                earthquakes_within_area.append(earthquake)

        earthquake_ids_within_area = [earthquake.id for earthquake in earthquakes_within_area]
        queryset = Earthquake.objects.filter(id__in=earthquake_ids_within_area)
        filter_set = EarthquakeFilter(filtered_query_params, queryset=queryset)
        filtered_queryset = filter_set.qs[:200]
        serializer = EarthquakesSerializer(filtered_queryset, many=True)
        return Response(serializer.data)
    

class GetGoogleMapAPIKey(APIView):
    def get(self, request):
        google_map_api_key = settings.GOOGLE_MAP_API_KEY
        return Response({"GOOGLE_MAP_API_KEY": google_map_api_key})