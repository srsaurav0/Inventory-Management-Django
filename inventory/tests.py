from django.test import TestCase
from inventory.models import Location, Accommodation
from django.contrib.gis.geos import Point
from django.urls import reverse
from django.contrib.auth.models import Group, User
from django.db import connection


class LocationTestCase(TestCase):
    def test_location_creation(self):
        location = Location.objects.create(
            id="1",
            title="Test Country",
            center=Point(-100.0, 40.0),
            location_type="country",
            country_code="TC",
        )
        self.assertEqual(location.title, "Test Country")


class AccommodationTestCase(TestCase):
    def test_accommodation_creation(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="password123")

        # Create a location
        location = Location.objects.create(
            id="1",
            title="Test Country",
            center=Point(-100.0, 40.0),
            location_type="country",
            country_code="TC",
        )

        # Create an accommodation
        accommodation = Accommodation.objects.create(
            id="2",
            title="Test Property",
            country_code="TC",
            bedroom_count=2,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(-99.9, 40.1),
            location=location,
            user=user,  # Provide the user here
        )

        self.assertEqual(accommodation.title, "Test Property")
        self.assertEqual(accommodation.user.username, "testuser")

    def test_accommodation_partitioning(self):
        user = User.objects.create_user(username="testuser", password="password123")
        location = Location.objects.create(
            id="1",
            title="Test Location",
            center=Point(-100.0, 40.0),
            location_type="city",
            country_code="TC",
        )
        # Insert data with feed value
        accommodation = Accommodation.objects.create(
            id="101",
            feed=1,
            title="Partition Test",
            country_code="TC",
            bedroom_count=3,
            review_score=4.5,
            usd_rate=100.00,
            center=Point(-99.9, 40.1),
            location=location,
            user=user,
        )
        self.assertTrue(Accommodation.objects.filter(id="101").exists())

        # Validate that the data is routed to the correct partition
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM accommodation_feed_1 WHERE id = '101'")
            result = cursor.fetchone()
        self.assertIsNotNone(result)


class PropertyOwnerSignupTestCase(TestCase):
    def setUp(self):
        # Ensure the Property Owners group exists before each test
        self.property_owners_group, _ = Group.objects.get_or_create(name="Property Owners")

    def test_property_owner_signup_get(self):
        """Test GET request for the sign-up view."""
        response = self.client.get(reverse("property_owner_signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/signup.html")  # Verify correct template is used
        self.assertIn("Sign Up as a Property Owner", response.content.decode())

    def test_property_owner_signup_post_success(self):
        """Test successful POST request for the sign-up view."""
        # Ensure the Property Owners group exists
        Group.objects.get_or_create(name="Property Owners")

        # Create a superuser for admin access
        admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="admin123"
        )
        self.client.login(username="admin", password="admin123")  # Log in as admin

        # Perform the signup request
        response = self.client.post(reverse("property_owner_signup"), {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123",
            "first_name": "Test",
            "last_name": "User",
        })

        # Assertions for successful signup
        self.assertEqual(response.status_code, 302)  # Check for redirection
        self.assertRedirects(response, "/admin/")  # Ensure redirect to admin page
        self.assertTrue(User.objects.filter(username="testuser").exists())  # User should exist

        user = User.objects.get(username="testuser")
        self.assertTrue(user.groups.filter(name="Property Owners").exists())  # User in the group
        self.assertEqual(user.first_name, "Test")  # First name is correct
        self.assertEqual(user.last_name, "User")  # Last name is correct


    def test_property_owner_signup_post_failure(self):
        """Test POST request with invalid data."""
        response = self.client.post(reverse("property_owner_signup"), {
            "username": "",  # Missing required fields
            "email": "",
            "password": "",
        })

        # Assertions for failed signup
        self.assertEqual(response.status_code, 200)  # Form should re-render
        self.assertTemplateUsed(response, "inventory/signup.html")  # Verify the form is re-rendered
        self.assertIn("This field is required", response.content.decode())  # Check error message
        self.assertFalse(User.objects.exists())  # Ensure no user is created