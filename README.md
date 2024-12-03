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

apt-get update && apt-get install -y nano

nano /app/inventory/tests/test_models.py
nano /app/inventory/tests/test_views.py

ctrl + k

pytest --cov=inventory

pytest --cov=inventory --cov-report=term-missing

pytest --cov=inventory --cov-report=html

pytest --cov=inventory --cov-report term-missing --cov-config=.coveragerc

python manage.py generate_sitemap