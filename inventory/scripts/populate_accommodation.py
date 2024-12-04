from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point
import random

def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user5", email="user5@gmail.com")
    if created:
        user.set_password("password5")
        user.save()
        print("User 'user5' created.")
    else:
        print("User 'user5' already exists.")

    # Create Accommodations with Random Attributes
    accommodations = [
        {'id': '201', 'feed': 100, 'title': 'Modern Loft in NYC', 'bedroom_count': 2,
         'review_score': 4.5, 'usd_rate': 350.00, 'location_id': '12',
         'amenities': ['WiFi', 'City View', 'Air Conditioning', 'Parking']},
        {'id': '202', 'feed': 200, 'title': 'Beach House in Miami', 'bedroom_count': 3,
         'review_score': 4.8, 'usd_rate': 500.00, 'location_id': '25',
         'amenities': ['WiFi', 'Pool', 'Ocean View', 'BBQ Area']},
        {'id': '203', 'feed': 500, 'title': 'Rustic Cabin in Denver', 'bedroom_count': 4,
         'review_score': 4.3, 'usd_rate': 300.00, 'location_id': '23',
         'amenities': ['WiFi', 'Mountain View', 'Fireplace']},
        {'id': '204', 'feed': 1050, 'title': 'Elegant Apartment in Toronto', 'bedroom_count': 1,
         'review_score': 4.9, 'usd_rate': 400.00, 'location_id': '9',
         'amenities': ['WiFi', 'Gym', 'Elevator']},
        {'id': '205', 'feed': 2050, 'title': 'Penthouse in Vancouver', 'bedroom_count': 3,
         'review_score': 4.7, 'usd_rate': 550.00, 'location_id': '18',
         'amenities': ['WiFi', 'Balcony', 'City View']},
        # Add 15 more random accommodations as needed
    ]

    for acc in accommodations:
        location = Location.objects.get(id=acc['location_id'])
        Accommodation.objects.get_or_create(
            id=acc['id'], feed=acc['feed'], title=acc['title'], country_code=location.country_code,
            bedroom_count=acc['bedroom_count'], review_score=acc['review_score'],
            usd_rate=acc['usd_rate'], center=location.center, location=location,
            user=user, amenities=acc['amenities']
        )

    print("Data population completed successfully for user5!")

run()
