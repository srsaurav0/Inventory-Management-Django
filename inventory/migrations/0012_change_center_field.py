from django.contrib.gis.db import models as gis_models
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_add_image_file_field'),  # Replace with your latest migration file
    ]

    operations = [
        # Step 1: Add a temporary field to store the existing data
        migrations.AddField(
            model_name='accommodation',
            name='center_temp',
            field=gis_models.PointField(null=True, srid=4326),  # Temporary PointField
        ),

        # Step 2: Copy data from `center` to `center_temp`
        migrations.RunSQL("""
            UPDATE inventory_accommodation
            SET center_temp = ST_SetSRID(ST_Point(ST_X(center::geometry), ST_Y(center::geometry)), 4326)
        """),

        # Step 3: Drop the old `center` field
        migrations.RemoveField(
            model_name='accommodation',
            name='center',
        ),

        # Step 4: Rename `center_temp` to `center`
        migrations.RenameField(
            model_name='accommodation',
            old_name='center_temp',
            new_name='center',
        ),
    ]
