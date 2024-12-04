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
- **Partitioned Tables** for optimized database handling.
- **Testing with Coverage** using `pytest` and `coverage`.

---

## Installation

### Prerequisites
- Python 3.9 or higher
- PostgreSQL with PostGIS
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