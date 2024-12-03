import pytest
from django.urls import reverse
from django.contrib.auth.models import Group, User

@pytest.mark.django_db
def test_property_owner_signup_get(client):
    """Test GET request for the sign-up view."""
    response = client.get(reverse("property_owner_signup"))
    assert response.status_code == 200
    assert "Sign Up as a Property Owner" in response.content.decode()

@pytest.mark.django_db
def test_property_owner_signup_post_success(client):
    """Test successful POST request for the sign-up view."""
    # Ensure the Property Owners group exists
    Group.objects.get_or_create(name="Property Owners")

    # Submit the form with valid data
    response = client.post(reverse("property_owner_signup"), {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User",
    })

    # Assertions
    assert response.status_code == 200  # Render the same form with messages
    assert User.objects.filter(username="testuser").exists()
    user = User.objects.get(username="testuser")
    assert user.groups.filter(name="Property Owners").exists()
    assert user.first_name == "Test"
    assert user.last_name == "User"

@pytest.mark.django_db
def test_property_owner_signup_post_failure(client):
    """Test POST request with invalid data."""
    response = client.post(reverse("property_owner_signup"), {
        "username": "",  # Missing required fields
        "email": "",
        "password": "",
    })

    # Assertions
    assert response.status_code == 200
    assert "This field is required" in response.content.decode()
    assert not User.objects.exists()
