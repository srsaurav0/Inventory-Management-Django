from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_partition_localize_accommodation_default'),  # Replace with the correct dependency
    ]

    operations = [
        # Step 3.1: Rename the original table
        migrations.RunSQL("""
            ALTER TABLE inventory_accommodation RENAME TO inventory_accommodation_temp;
        """),

        # Step 3.2: Create the new range-partitioned table
        migrations.RunSQL("""
            CREATE TABLE inventory_accommodation (
                id VARCHAR(20) NOT NULL,
                feed INTEGER NOT NULL,
                title VARCHAR(100) NOT NULL,
                country_code VARCHAR(2) NOT NULL,
                bedroom_count INT NOT NULL,
                review_score NUMERIC(3, 1) DEFAULT 0,
                usd_rate NUMERIC(10, 2),
                center GEOGRAPHY(POINT, 4326),
                images JSONB DEFAULT '[]',
                amenities JSONB DEFAULT '[]',
                user_id INT NOT NULL,
                location_id VARCHAR(20) NOT NULL,
                published BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (id, feed)
            ) PARTITION BY RANGE (feed);
        """),

        migrations.RunSQL("""
            DROP TABLE IF EXISTS accommodation_feed_1;
            DROP TABLE IF EXISTS accommodation_feed_2;
            DROP TABLE IF EXISTS accommodation_feed_3;
            DROP TABLE IF EXISTS accommodation_feed_4;
        """),

        # Step 3.3: Create the new partitions
        migrations.RunSQL("""
            CREATE TABLE accommodation_feed_1 PARTITION OF inventory_accommodation
            FOR VALUES FROM (0) TO (1001);

            CREATE TABLE accommodation_feed_2 PARTITION OF inventory_accommodation
            FOR VALUES FROM (1001) TO (2001);

            CREATE TABLE accommodation_feed_3 PARTITION OF inventory_accommodation
            FOR VALUES FROM (2001) TO (3001);

            CREATE TABLE accommodation_feed_4 PARTITION OF inventory_accommodation
            FOR VALUES FROM (3001) TO (MAXVALUE);
        """),

        # Step 3.4: Migrate data from the temporary table
        migrations.RunSQL("""
            INSERT INTO inventory_accommodation (
                id, feed, title, country_code, bedroom_count, review_score, usd_rate,
                center, images, amenities, user_id, location_id, published, created_at, updated_at
            )
            SELECT
                id, feed, title, country_code, bedroom_count, review_score, usd_rate,
                center, images, amenities, user_id, location_id, published, created_at, updated_at
            FROM inventory_accommodation_temp;
        """),

        # Step 3.5: Drop the temporary table
        migrations.RunSQL("""
            DROP TABLE inventory_accommodation_temp;
        """),
    ]
