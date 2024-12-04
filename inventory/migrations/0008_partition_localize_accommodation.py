from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_add_image_file_field'),  # Replace with your latest migration
    ]

    operations = [
        # Step 3.1: Rename the original table
        migrations.RunSQL("""
            ALTER TABLE inventory_localizeaccommodation RENAME TO inventory_localizeaccommodation_temp;
        """),

        # Step 3.2: Create the new partitioned table
        migrations.RunSQL("""
            CREATE TABLE inventory_localizeaccommodation (
                id SERIAL NOT NULL,
                property_id VARCHAR(20) NOT NULL,
                language CHAR(2) NOT NULL,
                description TEXT,
                policy JSONB DEFAULT '{}',
                PRIMARY KEY (id, language)
            ) PARTITION BY LIST (language);
        """),

        # Step 3.3: Create partitions for each language
        migrations.RunSQL("""
            CREATE TABLE localize_accommodation_en PARTITION OF inventory_localizeaccommodation FOR VALUES IN ('EN');
            CREATE TABLE localize_accommodation_fr PARTITION OF inventory_localizeaccommodation FOR VALUES IN ('FR');
            CREATE TABLE localize_accommodation_es PARTITION OF inventory_localizeaccommodation FOR VALUES IN ('ES');
            CREATE TABLE localize_accommodation_bd PARTITION OF inventory_localizeaccommodation FOR VALUES IN ('BD');
        """),

        # Step 3.4: Migrate data from the temporary table
        migrations.RunSQL("""
            INSERT INTO inventory_localizeaccommodation (
                id, property_id, language, description, policy
            )
            SELECT id, property_id, language, description, policy
            FROM inventory_localizeaccommodation_temp;
        """),

        # Step 3.5: Drop the temporary table
        migrations.RunSQL("""
            DROP TABLE inventory_localizeaccommodation_temp;
        """),
    ]
