from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

def run():
    # Create a user
    user, created = User.objects.get_or_create(username='property_owner')
    if created:
        user.set_password('password123')
        user.save()

    # Create Countries
    usa, _ = Location.objects.get_or_create(
        id='1',
        title='USA',
        center=Point(-100.0, 40.0),
        location_type='country',
        country_code='US'
    )
    canada, _ = Location.objects.get_or_create(
        id='2',
        title='Canada',
        center=Point(-106.3468, 56.1304),
        location_type='country',
        country_code='CA'
    )

    # Create States
    california, _ = Location.objects.get_or_create(
        id='3',
        title='California',
        center=Point(-119.4179, 36.7783),
        location_type='state',
        country_code='US',
        parent=usa
    )
    texas, _ = Location.objects.get_or_create(
        id='4',
        title='Texas',
        center=Point(-99.9018, 31.9686),
        location_type='state',
        country_code='US',
        parent=usa
    )
    ontario, _ = Location.objects.get_or_create(
        id='5',
        title='Ontario',
        center=Point(-85.3232, 50.0000),
        location_type='state',
        country_code='CA',
        parent=canada
    )
    quebec, _ = Location.objects.get_or_create(
        id='6',
        title='Quebec',
        center=Point(-71.2082, 46.8139),
        location_type='state',
        country_code='CA',
        parent=canada
    )

    # Create Cities
    los_angeles, _ = Location.objects.get_or_create(
        id='7',
        title='Los Angeles',
        center=Point(-118.2437, 34.0522),
        location_type='city',
        country_code='US',
        parent=california
    )
    toronto, _ = Location.objects.get_or_create(
        id='9',
        title='Toronto',
        center=Point(-79.3832, 43.6532),
        location_type='city',
        country_code='CA',
        parent=ontario
    )

    # Create Accommodations
    Accommodation.objects.get_or_create(
        id='11',
        title='Luxury Apartment in LA',
        country_code='US',
        bedroom_count=3,
        review_score=4.8,
        usd_rate=250.00,
        center=Point(-118.2437, 34.0522),
        location=los_angeles,
        user=user
    )
    Accommodation.objects.get_or_create(
        id='12',
        title='Cozy Condo in Toronto',
        country_code='CA',
        bedroom_count=2,
        review_score=4.5,
        usd_rate=180.00,
        center=Point(-79.3832, 43.6532),
        location=toronto,
        user=user
    )

    print("Data population completed successfully!")
