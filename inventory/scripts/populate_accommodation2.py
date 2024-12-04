from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user6", email="user6@gmail.com")
    if created:
        user.set_password("password6")
        user.save()
        print("User 'user6' created.")
    else:
        print("User 'user6' already exists.")

    # Create Accommodations with Random Attributes
    accommodations = [
        {'id': '301', 'feed': 1500, 'title': 'Cozy Apartment in London', 'bedroom_count': 1,
         'review_score': 4.6, 'usd_rate': 250.00, 'location_id': '47',
         'amenities': ['WiFi', 'Heating', 'Parking']},
        {'id': '302', 'feed': 3001, 'title': 'Luxury Villa in Sydney', 'bedroom_count': 5,
         'review_score': 4.9, 'usd_rate': 800.00, 'location_id': '48',
         'amenities': ['WiFi', 'Pool', 'Ocean View', 'BBQ Area']},
        # Add more random accommodations as needed
    ]

    for acc in accommodations:
        location = Location.objects.get(id=acc['location_id'])
        Accommodation.objects.get_or_create(
            id=acc['id'], feed=acc['feed'], title=acc['title'], country_code=location.country_code,
            bedroom_count=acc['bedroom_count'], review_score=acc['review_score'],
            usd_rate=acc['usd_rate'], center=location.center, location=location,
            user=user, amenities=acc['amenities']
        )

    print("Data population completed successfully for user6!")

run()
