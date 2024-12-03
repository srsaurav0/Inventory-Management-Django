from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Location, Accommodation, LocalizeAccommodation, AccommodationImage
from django.utils.html import mark_safe


@admin.register(Location)
class LocationAdmin(LeafletGeoAdmin):
    list_display = ("id", "title", "country_code", "location_type", "created_at", "updated_at")
    search_fields = ("title", "country_code")
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
    list_display = ("id", "title", "country_code", "published", "image_preview")
    search_fields = ("title", "country_code")
    list_filter = ("published", "country_code")
    fields = (
        "id",
        "title",
        "country_code",
        "bedroom_count",
        "review_score",
        "usd_rate",
        "center",
        "images",
        "amenities",
        "published",
        "image_preview",
    )
    readonly_fields = ("image_preview",)
    inlines = [AccommodationImageInline]

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
        if request.user.is_superuser:
            return qs  # Allow superusers to see all accommodations
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
