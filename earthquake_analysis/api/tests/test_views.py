import pytest
from rest_framework.test import APIClient
from ..models import Earthquake

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_earthquakes_filter_by_latitude(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'latitude__lt': 40})

    assert response.status_code == 200
    assert len(response.data) == 2

@pytest.mark.django_db
def test_earthquakes_filter_by_longitude(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'longitude__gt': -100})

    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_earthquakes_filter_by_multiple_parameters(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'longitude__gt': -100})

    assert response.status_code == 200
    assert len(response.data) == 1

@pytest.mark.django_db
def test_earthquakes_filter_by_invalid_parameters(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'latitude__gt': 40})
    assert response.status_code == 400
    assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'latitude'"}

@pytest.mark.django_db
def test_earthquakes_filter_by_date(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

    response = api_client.get('/api/earthquakes/', {'date__lt': '2021-02-01'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['date'] == '2021-01-01'

@pytest.mark.django_db
def test_earthquakes_filter_by_unavailable_date(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

    response = api_client.get('/api/earthquakes/', {'date__lt': '2021-01-01'})

    assert response.status_code == 200
    assert len(response.data) == 0

@pytest.mark.django_db
def test_earthquakes_filter_by_date_invalid_format(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

    response = api_client.get('/api/earthquakes/', {'date__lt': '2021/01/01'})

    assert response.status_code == 400
    assert response.data == {"Error": "Invalid date format. Use 'YYYY-MM-DD'"}

@pytest.mark.django_db
def test_earthquakes_filter_by_date_invalid_date_range(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-02-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-03-01')

    response = api_client.get('/api/earthquakes/', {'date__lt': '2021-01-01', 'date__gt': '2021-03-01'})

    assert response.status_code == 400
    assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'date'"}

@pytest.mark.django_db
def test_earthquakes_filter_by_magnitude_invalid_range(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'magnitude__lt': 5, 'magnitude__gt': 7})

    assert response.status_code == 400
    assert response.data == {"Error": "Cannot use 'lt' or 'gt' filters along with 'magnitude'"}

@pytest.mark.django_db
def test_earthquakes_filter_by_negative_depth(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0)

    response = api_client.get('/api/earthquakes/', {'depth__lt': 0})

    assert response.status_code == 400
    assert response.data == {"Error": "Depth cannot be negative"}

@pytest.mark.django_db
def test_earthquakes_filter_by_more_than_nine_magnitude(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=2.2)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.7)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=9)

    response = api_client.get('/api/earthquakes/', {'magnitude__gt': 9})

    assert response.status_code == 400
    assert response.data == {"Error": "Magnitude cannot be more than 9"}

@pytest.mark.django_db
def test_earthquakes_filter_by_negative_magnitude(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=2.2)
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.7)
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=-9)

    response = api_client.get('/api/earthquakes/', {'magnitude__lt': 0})

    assert response.status_code == 400
    assert response.data == {"Error": "Magnitude cannot be negative"}

@pytest.mark.django_db
def test_earthquakes_filter_by_all_parameters(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-01-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=5.0, date='2021-01-01')

    response = api_client.get('/api/earthquakes/', {'latitude__lt': 40, 'longitude__gt': -100, 'date__lt': '2021-02-01', 'magnitude__lt': 6})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['date'] == '2021-01-01'

@pytest.mark.django_db
def test_earthquakes_filter_by_no_parameters(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2021-01-01')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2021-01-01')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2021-01-01')

    response = api_client.get('/api/earthquakes/')

    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_earthquakes_year_list_view(api_client):

    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

    response = api_client.get('/api/earthquakes/date/')
    assert response.status_code == 200
    assert len(response.data) == 3

@pytest.mark.django_db
def test_earthquakes_year_list_view_with_year(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

    response_with_year = api_client.get('/api/earthquakes/date/', {'year': '2024'})
    assert response_with_year.status_code == 200
    assert len(response_with_year.data) == 3

@pytest.mark.django_db
def test_earthquakes_year_list_view_with_month(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2023-05-11')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2022-05-14')

    response_with_month = api_client.get('/api/earthquakes/date/', {'month': '06'})
    assert response_with_month.status_code == 200
    assert len(response_with_month.data) == 0

@pytest.mark.django_db
def test_earthquakes_year_list_view_with_day(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2023-04-11')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-11')

    response_with_day = api_client.get('/api/earthquakes/date/', {'day': '11'})
    assert response_with_day.status_code == 200
    assert len(response_with_day.data) == 2
    assert response_with_day.data[0]['latitude'] == 40.0

@pytest.mark.django_db
def test_earthquakes_year_list_view_with_year_month_day(api_client):
    Earthquake.objects.create(latitude=40.0, longitude=-74.0, depth=10, magnitude=5.0, date='2024-05-11')
    Earthquake.objects.create(latitude=35.0, longitude=-118.0, depth=15, magnitude=6.0, date='2024-05-13')
    Earthquake.objects.create(latitude=30.0, longitude=-80.0, depth=20, magnitude=7.0, date='2024-05-14')

    response_with_date = api_client.get('/api/earthquakes/date/', {'year': '2024', 'month': '05', 'day': '13'})
    assert response_with_date.status_code == 200
    assert len(response_with_date.data) == 1
    assert response_with_date.data[0]['latitude'] == 35.0 

