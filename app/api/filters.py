import django_filters
from app.models import Account, Transfer


class AccountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = {
            'open_date': ['gte', 'lte'],
            'type': ['exact'],
            'customer__id': ['exact']
        }


class TransferFilter(django_filters.FilterSet):
    class Meta:
        model = Transfer
        fields = {
            'transfer_from__id': ['exact'],
            'transfer_to__id': ['exact'],
            'processing_date': ['gte', 'lte'],
            'amount': ['gte', 'lte', 'exact']
        }
