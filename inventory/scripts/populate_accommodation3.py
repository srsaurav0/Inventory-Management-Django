from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user7", email="user7@gmail.com")
    if created:
        user.set_password("password7")
        user.save()
        print("User 'user7' created.")
    else:
        print("User 'user7' already exists.")

    # Create Accommodations with Random Attributes
    accommodations = [
        {'id': '401', 'feed': 3400, 'title': 'Modern Flat in Beijing', 'bedroom_count': 2,
         'review_score': 4.4, 'usd_rate': 320.00, 'location_id': '71',
         'amenities': ['WiFi', 'Gym', 'City View']},
        {'id': '402', 'feed': 2300, 'title': 'Charming House in Bangkok', 'bedroom_count': 4,
         'review_score': 4.5, 'usd_rate': 280.00, 'location_id': '81',
         'amenities': ['WiFi', 'Pool', 'Garden']},
        # Add 18 more random accommodations as needed
    ]

    for acc in accommodations:
        location = Location.objects.get(id=acc['location_id'])
        Accommodation.objects.get_or_create(
            id=acc['id'], feed=acc['feed'], title=acc['title'], country_code=location.country_code,
            bedroom_count=acc['bedroom_count'], review_score=acc['review_score'],
            usd_rate=acc['usd_rate'], center=location.center, location=location,
            user=user, amenities=acc['amenities']
        )

    print("Data population completed successfully for user7!")

run()
