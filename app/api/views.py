from django.db.models import Q
from django.db.models.expressions import F
from django.db import transaction

from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from app.models import (Customer, Account, Transfer, Deposit, Withdraw)
from app.api.serializers import (CustomerSerializer, AccountSerializer, TransferSerializer, WithdrawSerializer,
                                 DepositSerializer)
from app.api.filters import AccountFilter, TransferFilter


class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class AccountCreateAPIView(APIView):

    def post(self, request):
        """
        {
            "customer":1,
            "account_type": "vadeli",
            "deposit_amount":20,
            "is_active": true
        }
        """
        with transaction.atomic():
            account_serializer = AccountSerializer(data=request.data)
            if account_serializer.is_valid(raise_exception=True):
                account_serializer.save()
            else:
                return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            deposit_serializer = DepositSerializer(data={'account': account_serializer.data["id"],
                                                         'amount': account_serializer.data['balance']})
            if deposit_serializer.is_valid(raise_exception=True):
                deposit_serializer.save()
            else:
                return Response(deposit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(account_serializer.data, status=status.HTTP_201_CREATED)


class AccountDetailAPIView(APIView):

    def get_object(self, id):
        account_instance = get_object_or_404(Account, id=id)
        return account_instance

    def get(self, request, id):
        account = self.get_object(id=id)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        account = self.get_object(id=id)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        account = self.get_object(id=id)
        account.is_active = False
        account.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AccountTransfersAPIView(APIView):

    def get_object(self, id):
        account_instance = get_object_or_404(Account, id=id)
        return account_instance

    def get(self, request, id):
        account = self.get_object(id=id)
        transfers = Transfer.objects.filter(Q(transfer_from=account) | Q(transfer_to=account))
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data)


class AccountListAPIView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        queryset = AccountFilter(self.request.query_params, queryset=self.queryset).qs
        return queryset


class TransferAPIView(APIView):

    def get(self, request):
        transfers = Transfer.objects.all().order_by("-processing_date")
        transfers = TransferFilter(request.GET, queryset=transfers).qs
        serializer = TransferSerializer(transfers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        {
            "amount": 50,
            "transfer_from": 10,
            "transfer_to":9
        }
        """
        with transaction.atomic():
            serializer = TransferSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serializer.validated_data['transfer_from'].balance = F('balance') - serializer.validated_data.get(
                    'amount')
                serializer.validated_data['transfer_to'].balance = F('balance') + serializer.validated_data.get(
                    'amount')
                serializer.validated_data['transfer_from'].save()
                serializer.validated_data['transfer_to'].save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepositListCreateAPIView(APIView):

    def post(self, request):
        """
        {
            "amount": 50,
            "account": 9
        }
        """
        with transaction.atomic():
            serializer = DepositSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                account = serializer.validated_data.get('account')
                account.balance += serializer.validated_data.get('amount')
                account.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawListCreateAPIView(APIView):
    """
        {
            "amount": 50,
            "account": 9
        }
    """

    def post(self, request):
        """
        {
            "amount": 50,
            "account": 9
        }
        """
        with transaction.atomic():
            serializer = WithdrawSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                account = serializer.validated_data.get('account')
                account.balance -= serializer.validated_data.get('amount')
                account.save()
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
