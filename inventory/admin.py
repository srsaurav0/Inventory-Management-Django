import csv
from django.urls import path
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import admin, messages
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation, AccommodationImage
from django.utils.html import mark_safe


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ("id", "title", "country_code", "location_type", "created_at", "updated_at")
    search_fields = ("title", "country_code")
    change_list_template = "admin/inventory/location_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name="location_import_csv"),
        ]
        return custom_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            try:
                decoded_file = csv_file.read().decode("utf-8")
                reader = csv.DictReader(decoded_file.splitlines())
                for row in reader:
                    Location.objects.create(
                        id=row["id"],
                        title=row["title"],
                        center=row["center"],  # Make sure this is in WKT or compatible format
                        location_type=row["location_type"],
                        country_code=row["country_code"],
                        state_abbr=row.get("state_abbr", ""),
                        city=row.get("city", ""),
                    )
                self.message_user(request, "Locations imported successfully!", level=messages.SUCCESS)
            except Exception as e:
                self.message_user(request, f"Error importing locations: {e}", level=messages.ERROR)

            return HttpResponseRedirect("../")  # Redirect back to the admin page

        return render(request, "admin/inventory/import_csv.html", context={})

    fields = (
        "id",
        "title",
        "country_code",
        "location_type",
        "parent",
        "state_abbr",
        "city",
        "center",
        "created_at",
        "updated_at",
    )
    readonly_fields = ("created_at", "updated_at")


class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1  # Allow adding one image by default


@admin.register(Accommodation)
class AccommodationAdmin(LeafletGeoAdmin):
    list_display = ("id", "title", "country_code", "location_title","published", "image_preview")
    search_fields = ("title", "country_code")
    list_filter = ("published", "country_code")
    fields = (
        "id",
        "title",
        "feed",
        "country_code",
        "location",
        "bedroom_count",
        "review_score",
        "usd_rate",
        "center",
        "images",
        "amenities",
        "published",
        "created_at",
        "updated_at",
        "image_preview",
    )
    readonly_fields = ("image_preview", "created_at", "updated_at")
    inlines = [AccommodationImageInline]

    def location_title(self, obj):
        return obj.location.title
    location_title.short_description = "Location"

    def image_preview(self, obj):
        """Display all uploaded images as thumbnails."""
        images = obj.uploaded_images.all()
        if not images:
            return "No images uploaded"
        return mark_safe(
            "".join(
                [
                    f'<img src="{img.image_file.url}" style="max-height: 100px; margin-right: 10px;"/>'
                    for img in images
                ]
            )
        )

    image_preview.short_description = "Image Previews"

    def save_model(self, request, obj, form, change):
        """Save the Accommodation instance."""
        if change and "location" in form.changed_data:  # If the location field is changed
            obj.country_code = obj.location.country_code
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        """Save related AccommodationImage objects and update the `images` field."""
        super().save_related(request, form, formsets, change)
        # Update the `images` JSON field after related objects are saved
        form.instance.images = [
            img.image_file.url for img in form.instance.uploaded_images.all()
        ]
        form.instance.save()

    def get_queryset(self, request):
        """Restrict displayed accommodations to those owned by the user."""
        qs = super().get_queryset(request)
        print(f"Superuser: {request.user.is_superuser}, User: {request.user}")
        if request.user.is_superuser:
            return qs  # Allow superusers to see all accommodations
        print(f"Filtered Queryset for user {request.user}: {qs.filter(user=request.user)}")
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        """Restrict update access to the owner of the accommodation."""
        if request.user.is_superuser:
            return True  # Superusers can edit anything
        if obj and obj.user != request.user:
            return False  # Users cannot edit others' accommodations
        return True

    # def has_delete_permission(self, request, obj=None):
    #     """Restrict delete access to the owner of the accommodation."""
    #     if request.user.is_superuser:
    #         return True
    #     if obj and obj.user != request.user:
    #         return False
    #     return True

    def has_view_permission(self, request, obj=None):
        """Restrict view access to the owner of the accommodation."""
        if request.user.is_superuser:
            return True
        if obj and obj.user != request.user:
            return False
        return True


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "language")
    search_fields = ("property__title", "language")
