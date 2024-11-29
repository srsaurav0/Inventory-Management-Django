import pytest
from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

@pytest.mark.django_db
def test_location_creation():
    location = Location.objects.create(
        id='1',
        title='Test Country',
        center=Point(-100.0, 40.0),
        location_type='country',
        country_code='TC'
    )
    assert location.title == 'Test Country'

@pytest.mark.django_db
def test_accommodation_creation():
    # Create a test user
    user = User.objects.create_user(username='testuser', password='password123')

    # Create a location
    location = Location.objects.create(
        id='1',
        title='Test Country',
        center=Point(-100.0, 40.0),
        location_type='country',
        country_code='TC'
    )

    # Create an accommodation
    accommodation = Accommodation.objects.create(
        id='2',
        title='Test Property',
        country_code='TC',
        bedroom_count=2,
        review_score=4.5,
        usd_rate=100.00,
        center=Point(-99.9, 40.1),
        location=location,
        user=user  # Provide the user here
    )

    assert accommodation.title == 'Test Property'
    assert accommodation.user.username == 'testuser'
