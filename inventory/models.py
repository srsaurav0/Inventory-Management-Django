from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.contrib.gis.db import models

class Location(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    center = models.PointField()  # PostGIS Point field
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    location_type = models.CharField(max_length=20)
    country_code = models.CharField(max_length=2)
    state_abbr = models.CharField(max_length=3, blank=True)
    city = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Accommodation(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    feed = models.PositiveSmallIntegerField(default=0)
    title = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    bedroom_count = models.PositiveIntegerField()
    review_score = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    usd_rate = models.DecimalField(max_digits=10, decimal_places=2)
    center = models.PointField()
    images = models.JSONField(default=list, blank=True)
    image_file = models.ImageField(upload_to='accommodation_images/', null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amenities = models.JSONField(default=list)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(
        'Accommodation', related_name='uploaded_images', on_delete=models.CASCADE
    )
    image_file = models.ImageField(upload_to='accommodation_images/')


class LocalizeAccommodation(models.Model):
    id = models.AutoField(primary_key=True)
    property = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    language = models.CharField(max_length=2)
    description = models.TextField()
    policy = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.property.title} - {self.language}"
    

# Signal to add new users to the Property Owners group
@receiver(post_save, sender=User)
def add_to_property_owners_group(sender, instance, created, **kwargs):
    if created:  # Only for new users
        property_owners_group, _ = Group.objects.get_or_create(name="Property Owners")
        instance.groups.add(property_owners_group)
