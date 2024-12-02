from django.contrib import admin
from .models import Location, Accommodation, LocalizeAccommodation, AccommodationImage
from django.utils.html import mark_safe


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "location_type", "country_code")
    search_fields = ("title", "country_code")


class AccommodationImageInline(admin.TabularInline):
    model = AccommodationImage
    extra = 1  # Allow adding one image by default
    

@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
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

    image_preview.allow_tags = True
    image_preview.short_description = "Image Previews"

    def save_model(self, request, obj, form, change):
        """Update JSON images field with all uploaded image URLs."""
        # Collect all URLs from related AccommodationImage instances
        obj.images = [img.image_file.url for img in obj.uploaded_images.all()]
        super().save_model(request, obj, form, change)


@admin.register(LocalizeAccommodation)
class LocalizeAccommodationAdmin(admin.ModelAdmin):
    list_display = ("id", "property", "language")
    search_fields = ("property__title", "language")
