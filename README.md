# Property Management System - Django Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Key Files](#key-files)
- [Testing](#testing)
- [Partitioning](#testing)

---

## Introduction

This Django-based Property Management System (PMS) allows users to manage accommodations and locations while providing a custom admin interface. It includes features such as CSV import, geospatial data handling with Leaflet, and advanced user-specific permissions.

---

## Features

- **CRUD Operations** for locations and accommodations.
- **Custom Admin Panel** for importing locations from CSV files.
- **Geospatial Data Handling** with Django's `PostGIS` and Leaflet integration.
- **Custom Permissions** to restrict access based on ownership.
- **Image Uploads and Previews** for accommodations.
- **Dynamic Sitemap Generation** for all locations and their nested hierarchies.
- **Partitioned Tables** for optimized database handling.
- **Testing with Coverage** using `django.test`.
- **Integration** of `Docker` for seamless deployment.

---

## Installation

### Prerequisites
- Python 3.9 or higher (Check with command `python3 --version`)
- Docker & Docker-Compose (Check with command `docker-compose --version`)
- Virtual environment (recommended)

### Steps
1. Clone the repository:
   ```bash
    git clone https://github.com/srsaurav0/Inventory-Management-Django.git
    cd Inventory-Management-Django
   ```
2. Create and activate a virtual environment:
   On Linux:
   ```bash
    python3 -m venv .venv
    source .venv/bin/activate
   ```
   On Windows:
   ```bash
    python -m venv .venv
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    .venv\Scripts\activate
   ```
3. Build and run docker:
   ```bash
    docker-compose up --build
   ```
   This will start two images named:
   - django_web
   - postgres_container
4. Apply migrations:
   Open another terminal and enter the virtual environment (.venv) similarly like before. Then apply migrations inside docker container.
   ```bash
    docker exec -it django_web bash
    python manage.py migrate
   ```
5. Create a Superuser:
   ```bash
    python manage.py createsuperuser
   ```
6. Access the Application:
   - Admin panel: `localhost:8000/admin/`
   - User panel: `localhost:8000`


---

## Usage

### Adding Locations via CSV
1. Navigate to the Django Admin panel in website `localhost:8000/admin/` and log in.
2. Click the `Locations` tab.
3. Click the `Import Locations from CSV` button in the top right corner for adding locations.
4. Upload a properly formatted CSV file named `location_data.csv` in path ***Inventory-Management-Django\location_data.csv***.

### Generating Sitemap
Run the command:
   ```bash
    python manage.py generate_sitemap
   ```
This creates a `sitemap.json` file in the project root.

### Adding Users and Accommodations using Scripts
Scripts are located in ***Inventory-Management-Django\inventory\scripts\*** folder.
Run the command:
   ```bash
    python manage.py shell
    exec(open('inventory/scripts/populate_accommodation.py').read())
    exec(open('inventory/scripts/populate_accommodation2.py').read())
    exec(open('inventory/scripts/populate_accommodation3.py').read())
    exec(open('inventory/scripts/populate_data.py').read())
    exec(open('inventory/scripts/populate_data3.py').read())
    exec(open('inventory/scripts/populate_data4.py').read())
    exec(open('inventory/scripts/populate_la.py').read())
   ```
These commands will create 6 users with these **usernames**, **emails** and **passwords**:
 - **username**: "user1", **email**: "user1@gmail.com", **password**: "password1"
 - **username**: "user3", **email**: "user3@gmail.com", **password**: "password3"
 - **username**: "user4", **email**: "user4@gmail.com", **password**: "password4"
 - **username**: "user5", **email**: "user5@gmail.com", **password**: "password5"
 - **username**: "user6", **email**: "user6@gmail.com", **password**: "password6"
 - **username**: "user7", **email**: "user7@gmail.com", **password**: "password7"

It will also create localize accommodation entries.
Run command `python manage.py generate_sitemap` to create an updated **sitemap.json**

### Approving Users
1. Visit `http://localhost:8000/admin/` and log in as an admin.
2. Click on the `Users` and see if the `Staff Status` is active (Green Tick).
3. If not (Red Cross), then enter into his profile by clicking the `Username`.
4. Click the staff status to turn it on. Also, check if permissions to **add**, **change** and **view** *accommodation* and *accommodationimages* are provided. If not, then select these 6 permissions and click on the right arrow beside them.
5. Click the `save` button at the bottom of the page.

### Log In as User
1. Log out from the admin account and log in as an user with username and password.
2. To create a new user account, a user can visit page `http://localhost:8000` and sign in. A user can't sign in until his/her staff status is approved.
3. A user can log in from the admin login page which is `http://localhost:8000/admin/`.
4. After logging in, the user can view, edit or add only in the accommodation table that are uploaded by him. This condition is handled inside `admin.py` file.

### Viewing Property and Adding Images in Accommodation
1. First log in as user from `http://localhost:8000/admin/`.
2. Now a user can see all the accommodations uploaded by that user only. Selecet any accomodation to view the property and add images.
3. Navigate to the bottom portion of the page to find a field named **ACCOMMODATION IMAGES**. Initially there is only one option to upload an image. But the user can click the button **Add another Accommodation image** to add more images.
4. Click the **SAVE** button and then the images will be added. Additionally, urls will be generated for those images and saved inside the `Images` field.

 ---

## Project Structure

```bash
    Inventory-Management-Django/
    ├── inventory/                # Main app
    │   ├── admin.py              # Admin panel customization
    │   ├── models.py             # Database models
    │   ├── views.py         
    │   ├── forms.py           
    │   ├── urls.py          
    │   ├── tests.py              # Test cases
    │   ├── templates/            # HTML templates
    │   │   ├── admin/           
    │   │   │   └── import_csv.html
    │   │   │   └── location_change_list.html
    │   │   ├── inventory/         
    │   │   │   └── signup.html
    │   └── migrations/           # Database migrations
    │
    ├── inventory_management/     # Main project
    │   ├── asgi.py        
    │   ├── settings.py           
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── .gitignore
    ├── Dockerfile
    ├── docker-compose.yml
    ├── manage.py 
    ├── README.md 
    ├── location_data.csv
    ├── requirements.txt
    └── sitemap.json              # Sitemap for location data
```

---

## Key Files

### Models
- **Location**: Represents hierarchical locations with geospatial data.
- **Accommodation**: Stores property data, partitioned by feed.
- **LocalizeAccommodation**: Supports multilingual property descriptions. Partitioned by *country code*.

### Migrations
- **0006_auto_partitioning.py**: Implements partitioning for `Accommodation`.
- **0008_partition_localize_accommodation**: Implements partitioning for LocalizeAccommodation.
- **0010_change_feed_range.py**: Alters the `feed partitioning range` for Accommodation.

### Admin
- Enhanced Django Admin for user-friendly property and location management.
- Inlines for related models like `AccommodationImage`.


---

## Testing

### Run Tests
   ```bash
    python manage.py test
   ```
   If a message appears in console: `Type 'yes' if you would like to try deleting the test database 'test_inventory_management', or 'no' to cancel:`, then enter `yes`.

### Code Coverage
   ```bash
    coverage run manage.py test inventory
    coverage report
   ```

---

## Partitioning

### Partitioning Details

#### Accommodation Table
- Partitioned by `feed`:
  - 1-1000: `accommodation_feed_1`
  - 1001-2000: `accommodation_feed_2`
  - 2001-3000: `accommodation_feed_3`
  - 3001+: `accommodation_feed_4`

#### Localize Accommodation Table
- Partitioned by `language`:
  - Language-specific partitions (e.g., `en`, `fr`).
  - Default partition for other languages: `localize_accommodation_others`.

### Evaluate Partitioning

#### Access the PostgreSQL Database
   ```bash
    docker exec -it postgres_container bash
    psql -U user -d inventory_management
   ```
#### View Partition Details
   ```sql
    \d inventory_accommodation;
    \d inventory_localizeaccommodation;
   ```
#### List All Partitions
For Accommodation table:
   ```sql
    SELECT
        inhrelid::regclass AS partition_name,
        inhparent::regclass AS parent_name
    FROM pg_inherits
    WHERE inhparent::regclass = 'inventory_accommodation'::regclass;
   ```
For LocalizeAccommodation table:
   ```sql
    SELECT
        inhrelid::regclass AS partition_name,
        inhparent::regclass AS parent_name
    FROM pg_inherits
    WHERE inhparent::regclass = 'inventory_localizeaccommodation'::regclass;
   ```
#### Check Data Distribution
   ```sql
    SELECT * FROM accommodation_feed_1;
    SELECT * FROM accommodation_feed_2;
    SELECT * FROM accommodation_feed_3;
    SELECT * FROM accommodation_feed_4;
    SELECT * FROM localize_accommodation_en;
    SELECT * FROM localize_accommodation_es;
    SELECT * FROM localize_accommodation_bd;
    SELECT * FROM localize_accommodation_fr;
   ```