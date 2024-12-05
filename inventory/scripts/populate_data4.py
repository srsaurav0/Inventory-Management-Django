from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user4", email="user4@gmail.com")
    if created:
        user.set_password("password4")
        user.save()
        print("User 'user4' created.")
    else:
        print("User 'user4' already exists.")

    # Create Locations
    countries = [
        {'id': '631', 'title': 'Bangladesh', 'center': Point(90.4125, 23.8103), 'country_code': 'BD'},
    ]

    states = [
        {'id': '632', 'title': 'Dhaka Division', 'center': Point(90.4125, 23.8103), 'parent_id': '31', 'country_code': 'BD'},
        {'id': '633', 'title': 'Chittagong Division', 'center': Point(91.7832, 22.3569), 'parent_id': '31', 'country_code': 'BD'},
    ]

    cities = [
        {'id': '634', 'title': 'Dhaka', 'center': Point(90.4125, 23.8103), 'parent_id': '32', 'country_code': 'BD'},
        {'id': '635', 'title': 'Chittagong', 'center': Point(91.7832, 22.3569), 'parent_id': '33', 'country_code': 'BD'},
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
            'id': '636', 'feed': 3023, 'title': 'Luxury Apartment in Dhaka', 'bedroom_count': 3, 'review_score': 4.8, 
            'usd_rate': 200.00, 'location_id': '34', 
            'amenities': ['WiFi', 'Pool', 'City View', 'Parking']
        },
        {
            'id': '637', 'feed': 995, 'title': 'Seaside Villa in Chittagong', 'bedroom_count': 4, 'review_score': 4.9, 
            'usd_rate': 400.00, 'location_id': '35',
            'amenities': ['WiFi', 'Ocean View', 'BBQ Area', 'Air Conditioning']
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

    print("Data population completed successfully for user4!")

run()
