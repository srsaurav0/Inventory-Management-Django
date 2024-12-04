# Property Management System - Django Application

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Custom Admin Panel](#custom-admin-panel)
- [CSV Import](#csv-import)
- [Custom Permissions](#custom-permissions)
- [Testing](#testing)
- [Code Coverage](#code-coverage)
- [License](#license)

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
    git clone https://github.com/your-repository/property-management-system.git
    cd property-management-system
   ```
2. Create and activate a virtual environment:
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
   Open another terminal apply migrations inside docker container.
   ```bash
    docker exec -it django_web bash
    python manage.py migrate
   ```
5. Create a Superuser:
   ```bash
    python manage.py createsuperuser
   ```
6. Access the Application:
   - Admin panel: `http://localhost:8000/admin/`
   - User panel: `http://localhost:8000/`


---

## Usage

### Adding Locations via CSV
1. Navigate to the Django Admin panel.
2. Click the **Import CSV**"** button for locations.
3. Upload a properly formatted CSV file named `location_data.csv` in path ***Inventory-Management-Django\location_data.csv***.

### Generating Sitemap
Run the command:
   ```bash
    python manage.py generate_sitemap
   ```
This creates a `sitemap.json` file in the project root.