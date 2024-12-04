python3 -m venv .venv
source .venv/bin/activate

pip install django psycopg2-binary

docker-compose up --build
docker compose down


docker exec -it django_web bash

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

http://localhost:8000/signup/
http://localhost:8000/admin/


Accommodation.objects.all().delete()
Location.objects.all().delete()

python manage.py shell
exec(open('inventory/scripts/populate_data.py').read())
exec(open('inventory/scripts/add_accomodations.py').read())

apt-get update && apt-get install -y nano

nano /app/inventory/tests/test_models.py
nano /app/inventory/tests/test_views.py

ctrl + k

pytest --cov=inventory

pytest --cov=inventory --cov-report=term-missing

pytest --cov=inventory --cov-report=html

pytest --cov=inventory --cov-report term-missing --cov-config=.coveragerc

python manage.py generate_sitemap


CREATE TABLE accommodation_feed_1 PARTITION OF accommodation_partitioned FOR VALUES IN (1);
CREATE TABLE accommodation_feed_2 PARTITION OF accommodation_partitioned FOR VALUES IN (2);
CREATE TABLE accommodation_feed_3 PARTITION OF accommodation_partitioned FOR VALUES IN (3);
CREATE TABLE accommodation_feed_4 PARTITION OF accommodation_partitioned FOR VALUES IN (4);


RUN PSQL:

docker exec -it <postgres_container_name> bash
psql -U <postgres_user> <database_name>

psql -U user -d inventory_management


asgiref==3.8.1
coverage==7.6.8
Django==4.2.16
exceptiongroup==1.2.2
iniconfig==2.0.0
packaging==24.2
pluggy==1.5.0
psycopg2-binary==2.9.10
pytest==8.3.3
pytest-cov==6.0.0
pytest-django==4.9.0
sqlparse==0.5.2
tomli==2.2.1
typing_extensions==4.12.2
Pillow
django-leaflet