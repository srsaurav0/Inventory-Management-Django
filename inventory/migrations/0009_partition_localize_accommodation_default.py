from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0008_partition_localize_accommodation'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE TABLE localize_accommodation_others
            PARTITION OF inventory_localizeaccommodation
            DEFAULT;
        """),
    ]
