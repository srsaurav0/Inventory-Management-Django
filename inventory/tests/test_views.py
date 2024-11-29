import pytest
from django.urls import reverse
from django.contrib.auth.models import Group, User

@pytest.mark.django_db
def test_property_owner_signup_view(client):
    Group.objects.get_or_create(name='Property Owners')

    # Submit the sign-up form
    response = client.post(reverse('property_owner_signup'), {
        'username': 'testowner',
        'email': 'testowner@example.com',
        'password': 'password123'
    })

    # Assertions
    assert response.status_code == 302  # Redirect after success
    assert User.objects.filter(username='testowner').exists()  # Check if user is created
    user = User.objects.get(username='testowner')
    assert user.groups.filter(name='Property Owners').exists()  # Check if user is in the group
