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
                "locations": []
            }

            # Get child locations (e.g., states, cities)
            child_locations = Location.objects.filter(parent=country).order_by('title')
            for child in child_locations:
                child_data = {
                    child.title: f"{country.country_code.lower()}/{child.title.lower().replace(' ', '-')}"
                }
                country_data["locations"].append(child_data)

            sitemap.append(country_data)

        # Write to sitemap.json
        with open('sitemap.json', 'w') as file:
            json.dump(sitemap, file, indent=4)

        self.stdout.write(self.style.SUCCESS('Sitemap generated successfully!'))
