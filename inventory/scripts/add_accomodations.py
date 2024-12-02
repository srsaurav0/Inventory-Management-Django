from inventory.models import Accommodation, Location
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point


def run():
    print("Starting script to add accommodations for a new user...")

    # Create a new user
    print("Creating or fetching a new user...")
    user, created = User.objects.get_or_create(username="user2")
    if created:
        user.set_password("password2")
        user.email
        user.save()
        print("User 'new_user' created.")
    else:
        print("User 'new_user' already exists.")

    # Verify existing locations
    try:
        location_la = Location.objects.get(title="Los Angeles")
        location_toronto = Location.objects.get(title="Toronto")
        location_houston = Location.objects.get(title="Houston")
    except Location.DoesNotExist as e:
        print(
            "Error: Required locations not found in the database. Please populate locations first."
        )
        print(e)
        return

    # Add Accommodations
    accommodations = [
        {
            "id": "21",
            "title": "Modern Apartment in LA",
            "bedroom_count": 2,
            "review_score": 4.2,
            "usd_rate": 200.00,
            "location": location_la,
            "amenities": ["WiFi", "Pool", "Air Conditioning"],
            "images": ["https://example.com/images/la_modern1.jpg"],
        },
        {
            "id": "22",
            "title": "Luxury Condo in Toronto",
            "bedroom_count": 3,
            "review_score": 4.9,
            "usd_rate": 300.00,
            "location": location_toronto,
            "amenities": ["WiFi", "Gym", "Elevator"],
            "images": ["https://example.com/images/toronto_luxury1.jpg"],
        },
        {
            "id": "23",
            "title": "Spacious Villa in Houston",
            "bedroom_count": 4,
            "review_score": 4.7,
            "usd_rate": 400.00,
            "location": location_houston,
            "amenities": ["WiFi", "Private Pool", "Parking"],
            "images": ["https://example.com/images/houston_villa1.jpg"],
        },
    ]

    for acc in accommodations:
        Accommodation.objects.get_or_create(
            id=acc["id"],
            title=acc["title"],
            country_code=acc["location"].country_code,
            bedroom_count=acc["bedroom_count"],
            review_score=acc["review_score"],
            usd_rate=acc["usd_rate"],
            center=acc["location"].center,
            location=acc["location"],
            user=user,
            amenities=acc["amenities"],
            images=acc["images"],
        )
        print(f"Accommodation '{acc['title']}' added successfully.")

    print("Script completed successfully!")


run()
