import pytest
from django.db import IntegrityError
from ..models import Earthquake

@pytest.fixture
def sample_earthquake():
    return Earthquake.objects.create(
        event_id='test_event',
        date='2024-05-11',
        origin_time='12:00:00',
        latitude=12.345,
        longitude=67.890,
        depth=10.5,
        magnitude=5.0,
        md=4.5,
        ml=4.8,
        mw=5.2,
        ms=5.3,
        mb=5.1,
        event_type='earthquake',
        location='Test Location'
    )

# Check if the values are stored as float type
@pytest.mark.django_db
def test_float_values(sample_earthquake):
    assert isinstance(sample_earthquake.latitude, float)
    assert isinstance(sample_earthquake.longitude, float)
    assert isinstance(sample_earthquake.depth, float)
    assert isinstance(sample_earthquake.magnitude, float)
    assert isinstance(sample_earthquake.md, float)
    assert isinstance(sample_earthquake.ml, float)
    assert isinstance(sample_earthquake.mw, float)
    assert isinstance(sample_earthquake.ms, float)
    assert isinstance(sample_earthquake.mb, float)

# Check if magnitude and magnitudes fields are within 0<=x<=9
@pytest.mark.django_db
def test_magnitudes(sample_earthquake):
    try:
        assert 0 <= sample_earthquake.magnitude <= 9
        assert 0 <= sample_earthquake.md <= 9
        assert 0 <= sample_earthquake.ml <= 9
        assert 0 <= sample_earthquake.mw <= 9
        assert 0 <= sample_earthquake.ms <= 9
        assert 0 <= sample_earthquake.mb <= 9
    except IntegrityError:
        pytest.fail("IntegrityError raised when testing magnitudes.")


# Check if the magnitude field is less than zero
@pytest.mark.django_db
def test_magnitude_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.magnitude < 0 and sample_earthquake.magnitude > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the mw field is less than zero
@pytest.mark.django_db
def test_mw_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.mw < 0 and sample_earthquake.mw > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the ms field is less than zero
@pytest.mark.django_db
def test_ms_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.ms < 0 and sample_earthquake.ms > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the mb field is less than zero
@pytest.mark.django_db
def test_mb_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.mb < 0 and sample_earthquake.mb > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the ml field is less than zero
@pytest.mark.django_db
def test_ml_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.ml < 0 and sample_earthquake.ml > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the md field is less than zero
@pytest.mark.django_db
def test_md_is_out_of_the_range(sample_earthquake):
    if sample_earthquake.md < 0 and sample_earthquake.md > 9:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()
    
# Check if the date and origin_time fields are stored in correct format
@pytest.mark.django_db
def test_date_and_origin_time_format(sample_earthquake):
    # Check the format of the date field
    assert isinstance(sample_earthquake.date, str)  # Date field should be stored as a string
    assert sample_earthquake.date == '2024-05-11'    # Date should be stored in 'YYYY-MM-DD' format

    # Check the format of the origin_time field
    assert isinstance(sample_earthquake.origin_time, str)  # Origin time field should be stored as a string
    assert sample_earthquake.origin_time == '12:00:00'      # Origin time should be stored in 'HH:MM:SS' format

# Attempt to create an Earthquake object with the same event_id as the sample
@pytest.mark.django_db
def test_unique_event_id(sample_earthquake):
    with pytest.raises(IntegrityError):
        Earthquake.objects.create(
            event_id=sample_earthquake.event_id,  # Using the same event_id as the sample
            date='2024-05-11',
            origin_time='12:00:00',
            latitude=12.345,
            longitude=67.890,
            depth=10.5,
            magnitude=5.0,
            md=4.5,
            ml=4.8,
            mw=5.2,
            ms=5.3,
            mb=5.1,
            event_type='earthquake',
            location='Test Location'
        )

# Check if the __str__ method returns the location field
@pytest.mark.django_db
def test_str_method(sample_earthquake):
    assert str(sample_earthquake) == 'Test Location'

# Check if the depth field should be stored as a positive value
@pytest.mark.django_db
def test_depth_positive(sample_earthquake):
    if sample_earthquake.depth < 0:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

# Check if the latitude and longitude fields are within the valid range
@pytest.mark.django_db
def test_latitude_longitude_range(sample_earthquake):
    assert -90 <= sample_earthquake.latitude <= 90
    assert -180 <= sample_earthquake.longitude <= 180

# Check if latitude and longitude fields are outside the valid range
@pytest.mark.django_db
def test_latitude_outside_range(sample_earthquake):
    if sample_earthquake.latitude > 90 or sample_earthquake.latitude < -90:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()

@pytest.mark.django_db
def test_longitude_outside_range(sample_earthquake):
    if sample_earthquake.longitude > 180 or sample_earthquake.longitude < -180:
        with pytest.raises(IntegrityError):
            sample_earthquake.save()
