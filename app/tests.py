from django.test import TestCase
from django.urls import reverse
from app.models import (Customer, Account, Transfer, Deposit, Withdraw)
from app.api.serializers import (AccountSerializer, CustomerSerializer, TransferSerializer)
import json


class AccountTests(TestCase):
    print("test account apis and urls")

    def setUp(self):
        self.customer = Customer.objects.create(name="Emily Rodriguez",
                                                address="Example Address 3",
                                                identification_number="12345678903")

        self.account = Account.objects.create(customer=self.customer,
                                              balance=250,
                                              type='Deposit')

        self.valid_account_dict = json.dumps({
            "customer":self.customer.id,
            "type": "Deposit",
            "balance": 150.0,
            "is_active": False
        })
        self.invalid_account_dict = json.dumps({
            "type": 12,
            "balance": 150.0,
            "is_active": "Middle"
        })
        self.valid_create_account_dict = json.dumps({
            "customer": self.customer.id,
            "type": "Deposit",
            "balance": 200
        })
        self.invalid_create_account_dict = json.dumps({
            "customer": self.customer.id,
            "account_type": "Deposit"
        })

    def test_list_account(self):
        url = reverse("list-account")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_account(self):
        url = reverse("detail-account", kwargs={'id': self.account.id})
        response = self.client.get(url)
        serializer = AccountSerializer(self.account)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_valid_update_account(self):
        url = reverse("detail-account", kwargs={'id': self.account.id})
        response = self.client.put(url, data=self.valid_account_dict, content_type='application/json')
        serializer = AccountSerializer(self.account)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data, serializer.data)

    def test_invalid_update_account(self):
        url = reverse("detail-account", kwargs={'id': self.account.id})
        response = self.client.put(url, data=self.invalid_account_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_account(self):
        url = reverse("detail-account", kwargs={'id': self.account.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

    def test_valid_create_account(self):
        url = reverse("create-account")
        response = self.client.post(url, data=self.valid_create_account_dict, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_invalid_create_account(self):
        url = reverse("create-account")
        response = self.client.post(url, data=self.invalid_create_account_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_list_account_transfers(self):
        url = reverse("detail-account-transfer", kwargs={'id': self.account.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class CustomerTests(TestCase):
    print("test customer apis and urls")

    def setUp(self):
        self.customer = Customer.objects.create(name="Emily Rodriguez",
                                                address="Example Address 3",
                                                identification_number="12345678903")

        self.valid_customer_dict = json.dumps({
            "name": "Example Customer",
            "address": "Example Address 1",
            "identification_number": "12345678901"
        })
        self.invalid_customer_dict = json.dumps({
            "name": "Example Customer",
            "address": "Example Address 1",
            "identification_number": "*****678901"
        })

    def test_list_customer(self):
        url = reverse("list-create-customer")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_valid_create_customer(self):
        url = reverse("list-create-customer")
        response = self.client.post(url, data=self.valid_customer_dict, content_type='application/json')
        serializer = CustomerSerializer(json.loads(self.valid_customer_dict))
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data, serializer.data)

    def test_invalid_create_customer(self):
        url = reverse("list-create-customer")
        response = self.client.post(url, data=self.invalid_customer_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)


class TransfersTests(TestCase):
    print("test transfer apis and urls")

    def setUp(self):
        self.customer = Customer.objects.create(name="Emily Rodriguez",
                                                address="Example Address 3",
                                                identification_number="12345678903")

        self.from_account = Account.objects.create(customer=self.customer,
                                                   balance=250,
                                                   type='Deposit')

        self.to_account = Account.objects.create(customer=self.customer,
                                                 balance=10,
                                                 type='Deposit')

        self.transfer = Transfer.objects.create(amount=20,
                                                transfer_from=self.from_account,
                                                transfer_to=self.to_account)

        self.filter_dict = {
            "transfer_from__id": self.transfer.id
        }

        self.valid_transfer_dict = json.dumps({
            "amount": 100,
            "transfer_from": self.from_account.id,
            "transfer_to": self.to_account.id
        })
        self.invalid_transfer_dict = json.dumps({
            "amount": 5000,
            "transfer_from": self.from_account.id,
            "transfer_to": self.to_account.id
        })

    def test_list_transfers(self):
        url = reverse("transfer")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_transfers_with_filters(self):
        url = reverse("transfer")
        response = self.client.get(url, self.filter_dict)
        serializer = TransferSerializer(self.transfer)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], serializer.data)

    def test_valid_transfer_amount_between_different_accounts(self):
        url = reverse("transfer")
        response = self.client.post(url, data=self.valid_transfer_dict, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_invalid_transfer_amount_between_different_accounts(self):
        url = reverse("transfer")
        response = self.client.post(url, data=self.invalid_transfer_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)


class DepositTests(TestCase):
    print("test customer apis and urls")

    def setUp(self):
        self.customer = Customer.objects.create(name="Emily Rodriguez",
                                                address="Example Address 3",
                                                identification_number="12345678903")

        self.active_account = Account.objects.create(customer=self.customer,
                                                     balance=250,
                                                     type='Deposit')
        self.inactive_account = Account.objects.create(customer=self.customer,
                                                       balance=250,
                                                       type='Deposit',
                                                       is_active=False)

        self.valid_deposit_dict = json.dumps({
            "amount": 50,
            "account": self.active_account.id
        })
        self.invalid_deposit_dict = json.dumps({
            "amount": 50,
            "account": self.inactive_account.id
        })

    def test_valid_deposit_money(self):
        url = reverse("deposit")
        response = self.client.post(url, data=self.valid_deposit_dict, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_invalid_deposit_money(self):
        url = reverse("deposit")
        response = self.client.post(url, data=self.invalid_deposit_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)


class WithdrawTests(TestCase):
    print("test customer apis and urls")

    def setUp(self):
        self.customer = Customer.objects.create(name="Emily Rodriguez",
                                                address="Example Address 3",
                                                identification_number="12345678903")

        self.account = Account.objects.create(customer=self.customer,
                                              balance=250,
                                              type='Deposit')

        self.valid_withdraw_dict = json.dumps({
            "amount": 50,
            "account": self.account.id
        })
        self.invalid_withdraw_dict = json.dumps({
            "amount": 5000,
            "account": self.account.id
        })

    def test_valid_withdraw_money(self):
        url = reverse("withdraw")
        response = self.client.post(url, data=self.valid_withdraw_dict, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_invalid_withdraw_money(self):
        url = reverse("withdraw")
        response = self.client.post(url, data=self.invalid_withdraw_dict, content_type='application/json')
        self.assertEqual(response.status_code, 400)
