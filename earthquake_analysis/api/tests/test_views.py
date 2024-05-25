import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from ..models import Earthquake

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_earthquake():
    def _create_earthquake(latitude, longitude, depth, magnitude, date='2021-01-01'):
        return Earthquake.objects.create(latitude=latitude, longitude=longitude, depth=depth, magnitude=magnitude, date=date)
    return _create_earthquake

@pytest.mark.django_db
class TestEarthquakesFilterListView():
    def test_filter_by_latitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'latitude__lt': 40})

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_longitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'longitude__gt': -100})

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_multiple_parameters(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'longitude__gt': -100})

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_filter_by_invalid_parameters(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'latitude__gt': 40})
        assert response.status_code == 400
        assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'latitude'"}

    def test_filter_by_date(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

        response = api_client.get('/api/earthquakes/', {'date__lt': '2021-02-01'})

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['date'] == '2021-01-01'

    def test_filter_by_unavailable_date(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

        response = api_client.get('/api/earthquakes/', {'date__lt': '2021-01-01'})

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_filter_by_date_invalid_format(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

        response = api_client.get('/api/earthquakes/', {'date__lt': '2021/01/01'})

        assert response.status_code == 400
        assert response.data == {"Error": "Invalid date format. Use 'YYYY-MM-DD'"}

    def test_filter_by_date_invalid_date_range(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

        response = api_client.get('/api/earthquakes/', {'date__lt': '2021-01-01', 'date__gt': '2021-03-01'})

        assert response.status_code == 400
        assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'date'"}

    def test_filter_by_magnitude_invalid_range(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'magnitude__lt': 5, 'magnitude__gt': 7})

        assert response.status_code == 400
        assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'exact'"}

    def test_filter_by_negative_depth(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'depth__lt': 0})

        assert response.status_code == 400
        assert response.data == {"Error": "Depth cannot be negative"}

    def test_filter_by_more_than_nine_magnitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=2.2)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.7)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=9)

        response = api_client.get('/api/earthquakes/', {'magnitude__gt': 9})

        assert response.status_code == 400
        assert response.data == {"Error": "Magnitude cannot be more than 9"}

    def test_filter_by_negative_magnitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=2.2)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.7)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=-9)

        response = api_client.get('/api/earthquakes/', {'magnitude__lt': 0})

        assert response.status_code == 400
        assert response.data == {"Error": "Magnitude cannot be negative"}

    def test_filter_by_all_parameters(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-01-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=5.0, date='2021-01-01')

        response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'longitude__gt': -100, 'date__lt': '2021-02-01', 'magnitude__lt': 6})

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['date'] == '2021-01-01'

    def test_filter_by_no_parameters(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-01-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-01-01')

        response = api_client.get('/api/earthquakes/')

        assert response.status_code == 200
        assert len(response.data) == 3

@pytest.mark.django_db
class TestEarthquakesYearListView:
    def test_with_year(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

        response = api_client.get('/api/earthquakes/date/', {'year': '2024'})
        assert response.status_code == 200
        assert len(response.data) == 3

    def test_with_month(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

        response = api_client.get('/api/earthquakes/date/', {'month': '06'})
        assert response.status_code == 200
        assert len(response.data) == 0

    def test_with_day(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

        response = api_client.get('/api/earthquakes/date/', {'day': '11'})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['latitude'] == 40.0

    def test_with_year_month_day(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

        response = api_client.get('/api/earthquakes/date/', {'year': '2024', 'month': '05', 'day': '13'})
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['latitude'] == 35.0

    def test_filter_by_depth(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'depth__lt': 20})

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_date_range(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2022-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2022-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2022-03-01')

        response = api_client.get('/api/earthquakes/', {'date__gte': '2022-02-01', 'date__lte': '2022-03-01'})

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_filter_by_magnitude_range(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.5)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.5)

        response = api_client.get('/api/earthquakes/', {'magnitude__gt': 6, 'magnitude__lt': 7})

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_filter_by_negative_longitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'longitude__lt': -75})

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_date_and_magnitude(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2022-01-01')
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2022-02-01')
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2022-03-01')

        response = api_client.get('/api/earthquakes/', {'date__lt': '2022-03-01', 'magnitude__gte': 5})

        assert response.status_code == 200
        assert len(response.data) == 2

    def test_filter_by_latitude_and_longitude_range(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/', {'latitude__gt': 35, 'longitude__lt': -70})

        assert response.status_code == 200
        assert len(response.data) == 1

    def test_filter_by_missing_parameters(self, api_client):
        response = api_client.get('/api/earthquakes/')

        assert response.status_code == 200
        assert len(response.data) == 0

@pytest.mark.django_db
class TestEarthquakesWithinAnArea():
    def test_valid_input(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/list/', {'circle_center_lat': '35.0', 'circle_center_lng': '-100.0', 'circle_radius': '2000'})

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_invalid_input(self, api_client):
        response = api_client.get('/api/earthquakes/list/')

        assert response.status_code == 400
        assert response.data['error'] == 'circle_center_lat, circle_center_lng, and circle_radius are required.'

    def test_invalid_parameter_value(self, api_client):
        response = api_client.get('/api/earthquakes/list/', {'circle_center_lat': 'invalid', 'circle_center_lng': '100.0', 'circle_radius': '2000'})

        assert response.status_code == 400
        assert response.data['error'] == 'Invalid parameter value. Please provide valid numbers for circle_center_lat, circle_center_lng, and circle_radius.'

    def test_valid_input_with_results(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/list/', {'circle_center_lat': '35.0', 'circle_center_lng': '-100.0', 'circle_radius': '2000'})

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_valid_input_no_results(self, api_client):
        Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
        Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
        Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

        response = api_client.get('/api/earthquakes/list/', {'circle_center_lat': '45.0', 'circle_center_lng': '-100.0', 'circle_radius': '2000'})

        assert response.status_code == 200
        assert len(response.data) == 0

    def test_invalid_radius_parameter(self, api_client):
        response = api_client.get('/api/earthquakes/list/', {'circle_center_lat': '35.0', 'circle_center_lng': '-100.0', 'circle_radius': '-1'})

        assert response.status_code == 400
        assert response.data == {"error": "Invalid parameter value. Please provide a valid number for circle_radius."}
