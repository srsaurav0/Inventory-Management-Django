from inventory.models import Location, Accommodation
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point


def run():
    # Create a user if none exists
    user, created = User.objects.get_or_create(username="user1")
    if created:
        user.set_password("password1")
        user.save()
        print("User 'property_owner' created.")
    else:
        print("User 'property_owner' already exists.")

    # Create Locations
    countries = [
        {
            "id": "1",
            "title": "USA",
            "center": Point(-100.0, 40.0),
            "country_code": "US",
        },
        {
            "id": "2",
            "title": "Canada",
            "center": Point(-106.3468, 56.1304),
            "country_code": "CA",
        },
    ]

    states = [
        {
            "id": "3",
            "title": "California",
            "center": Point(-119.4179, 36.7783),
            "parent_id": "1",
            "country_code": "US",
        },
        {
            "id": "4",
            "title": "Texas",
            "center": Point(-99.9018, 31.9686),
            "parent_id": "1",
            "country_code": "US",
        },
        {
            "id": "5",
            "title": "Ontario",
            "center": Point(-85.3232, 50.0000),
            "parent_id": "2",
            "country_code": "CA",
        },
        {
            "id": "6",
            "title": "Quebec",
            "center": Point(-71.2082, 46.8139),
            "parent_id": "2",
            "country_code": "CA",
        },
    ]

    cities = [
        {
            "id": "7",
            "title": "Los Angeles",
            "center": Point(-118.2437, 34.0522),
            "parent_id": "3",
            "country_code": "US",
        },
        {
            "id": "8",
            "title": "Houston",
            "center": Point(-95.3698, 29.7604),
            "parent_id": "4",
            "country_code": "US",
        },
        {
            "id": "9",
            "title": "Toronto",
            "center": Point(-79.3832, 43.6532),
            "parent_id": "5",
            "country_code": "CA",
        },
        {
            "id": "10",
            "title": "Montreal",
            "center": Point(-73.5673, 45.5017),
            "parent_id": "6",
            "country_code": "CA",
        },
    ]

    for country in countries:
        Location.objects.get_or_create(
            id=country["id"],
            title=country["title"],
            center=country["center"],
            location_type="country",
            country_code=country["country_code"],
        )

    for state in states:
        parent = Location.objects.get(id=state["parent_id"])
        Location.objects.get_or_create(
            id=state["id"],
            title=state["title"],
            center=state["center"],
            location_type="state",
            country_code=state["country_code"],
            parent=parent,
        )

    for city in cities:
        parent = Location.objects.get(id=city["parent_id"])
        Location.objects.get_or_create(
            id=city["id"],
            title=city["title"],
            center=city["center"],
            location_type="city",
            country_code=city["country_code"],
            parent=parent,
        )

    # Create Accommodations
    accommodations = [
        {
            "id": "11",
            "title": "Luxury Apartment in LA",
            "bedroom_count": 3,
            "review_score": 4.8,
            "usd_rate": 250.00,
            "location_id": "7",
        },
        {
            "id": "12",
            "title": "Cozy Condo in Toronto",
            "bedroom_count": 2,
            "review_score": 4.5,
            "usd_rate": 180.00,
            "location_id": "9",
        },
    ]

    for acc in accommodations:
        location = Location.objects.get(id=acc["location_id"])
        Accommodation.objects.get_or_create(
            id=acc["id"],
            title=acc["title"],
            country_code=location.country_code,
            bedroom_count=acc["bedroom_count"],
            review_score=acc["review_score"],
            usd_rate=acc["usd_rate"],
            center=location.center,
            location=location,
            user=user,
        )

    print("Data population completed successfully!")
