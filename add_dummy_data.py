import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from app.api.serializers import CustomerSerializer

dummy_data = [
    {
        "id": 1,
        "name": "Sarah Johnson",
        "address": "Example Address 1",
        "identification_number": "12345678901"
    },
    {
        "id": 2,
        "name": "Michael Garcia",
        "address": "Example Address 2",
        "identification_number": "12345678902"
    },
    {
        "id": 3,
        "name": "Emily Rodriguez",
        "address": "Example Address 3",
        "identification_number": "12345678903"
    },
    {
        "id": 4,
        "name": "David Lee",
        "address": "Example Address 4",
        "identification_number": "12345678904"
    }
]

def create_data():
    serializer = CustomerSerializer(data=dummy_data,many=True)
    if serializer.is_valid():
        serializer.save()

create_data()