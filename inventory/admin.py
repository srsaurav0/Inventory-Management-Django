from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location_type', 'country_code')
    search_fields = ('title', 'country_code')

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country_code', 'published')
    search_fields = ('title', 'country_code')

@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ('id', 'property', 'language')
    search_fields = ('property__title', 'language')

