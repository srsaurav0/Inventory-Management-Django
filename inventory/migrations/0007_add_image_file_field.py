from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0006_auto_partitioning'),  # Replace with your last migration
    ]

    operations = [
        # Add the column to the parent table
        migrations.RunSQL("""
            ALTER TABLE inventory_accommodation ADD COLUMN image_file VARCHAR(100);
        """),
    ]
