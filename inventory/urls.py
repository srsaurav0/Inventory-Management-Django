from django.urls import path
from .views import PropertyOwnerSignUpView

urlpatterns = [
    path("", PropertyOwnerSignUpView.as_view(), name="property_owner_signup"),
]
