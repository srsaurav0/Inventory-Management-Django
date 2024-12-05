from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user3", email="user3@gmail.com")
    if created:
        user.set_password("password3")
        user.save()
        print("User 'user3' created.")
    else:
        print("User 'user3' already exists.")

    # Create Locations
    countries = [
        {'id': '621', 'title': 'UK', 'center': Point(-3.435973, 55.378051), 'country_code': 'GB'},
        {'id': '622', 'title': 'Australia', 'center': Point(133.775136, -25.274398), 'country_code': 'AU'},
    ]

    states = [
        {'id': '623', 'title': 'England', 'center': Point(-1.17432, 52.355518), 'parent_id': '21', 'country_code': 'GB'},
        {'id': '624', 'title': 'New South Wales', 'center': Point(151.2093, -33.8688), 'parent_id': '22', 'country_code': 'AU'},
    ]

    cities = [
        {'id': '625', 'title': 'London', 'center': Point(-0.127758, 51.507351), 'parent_id': '23', 'country_code': 'GB'},
        {'id': '626', 'title': 'Sydney', 'center': Point(151.2093, -33.8688), 'parent_id': '24', 'country_code': 'AU'},
    ]

    for country in countries:
        Location.objects.get_or_create(
            id=country['id'], title=country['title'], center=country['center'],
            location_type='country', country_code=country['country_code']
        )

    for state in states:
        parent = Location.objects.get(id=state['parent_id'])
        Location.objects.get_or_create(
            id=state['id'], title=state['title'], center=state['center'],
            location_type='state', country_code=state['country_code'], parent=parent
        )

    for city in cities:
        parent = Location.objects.get(id=city['parent_id'])
        Location.objects.get_or_create(
            id=city['id'], title=city['title'], center=city['center'],
            location_type='city', country_code=city['country_code'], parent=parent
        )

    # Create Accommodations with Amenities
    accommodations = [
        {
            'id': '627', 'feed': 507, 'title': 'Modern Flat in London', 'bedroom_count': 2, 'review_score': 4.7, 
            'usd_rate': 300.00, 'location_id': '25', 
            'amenities': ['WiFi', 'Heating', 'City View', 'Parking']
        },
        {
            'id': '628', 'feed': 2003, 'title': 'Beachside Villa in Sydney', 'bedroom_count': 4, 'review_score': 5.0, 
            'usd_rate': 500.00, 'location_id': '26',
            'amenities': ['WiFi', 'Pool', 'Ocean View', 'BBQ Area']
        },
    ]

    for acc in accommodations:
        location = Location.objects.get(id=acc['location_id'])
        Accommodation.objects.get_or_create(
            id=acc['id'], feed=acc['feed'], title=acc['title'], country_code=location.country_code,
            bedroom_count=acc['bedroom_count'], review_score=acc['review_score'],
            usd_rate=acc['usd_rate'], center=location.center, location=location, 
            user=user, amenities=acc['amenities']
        )

    print("Data population completed successfully for user3!")

run()
