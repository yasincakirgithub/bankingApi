echo "Create Migrations"
python manage.py makemigrations

echo "Start Migrate"
python manage.py migrate

echo "Add dummy data"
python add_dummy_data.py

echo "Start Project"
python manage.py runserver 0.0.0.0:8000

