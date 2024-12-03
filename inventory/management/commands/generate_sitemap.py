import json
from django.core.management.base import BaseCommand
from inventory.models import Location


class Command(BaseCommand):
    help = 'Generate a sitemap.json file for all country locations'

    def handle(self, *args, **options):
        # Get all country locations
        countries = Location.objects.filter(location_type='country').order_by('title')

        # Build the sitemap structure
        sitemap = []
        for country in countries:
            country_data = {
                country.title: country.country_code.lower(),
                "locations": self.get_child_locations(country, base_url=country.country_code.lower())
            }
            sitemap.append(country_data)

        # Write to sitemap.json
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=4)

        self.stdout.write(self.style.SUCCESS('Sitemap generated successfully!'))

    def get_child_locations(self, parent_location, base_url):
        """Recursively get all child locations with full hierarchy in the URL."""
        children = Location.objects.filter(parent=parent_location).order_by('title')
        child_data = []

        for child in children:
            full_url = f"{base_url}/{child.title.lower().replace(' ', '-')}"
            child_info = {
                child.title: full_url
            }

            # Only add "locations" if the child has further children
            grand_children = Location.objects.filter(parent=child).exists()
            if grand_children:
                child_info["locations"] = self.get_child_locations(child, base_url=full_url)

            child_data.append(child_info)

        return child_data
