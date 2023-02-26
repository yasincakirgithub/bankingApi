from rest_framework import serializers
from app.models import (Customer, Account, Transfer, Withdraw, Deposit)


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('__all__')

    def validate_identification_number(self, identification_number_value):
        if not len(identification_number_value) == 11:
            raise serializers.ValidationError(f'Identification number must be 11 digits.')
        if not identification_number_value.isdigit():
            raise serializers.ValidationError(
                f'The Identification number cannot contain any character type other than a digit.')
        return identification_number_value


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('customer', 'open_date', 'id', 'balance', 'type', 'is_active')
        read_only_fields = ('id','open_date')

    def validate_balance(self, balance_value):
        if balance_value < 50:
            raise serializers.ValidationError(f'Initial amount must be greater than 50')
        return balance_value


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('__all__')

    def validate(self, data):

        print(data["transfer_to"].is_active)
        print(data["transfer_from"].is_active)

        if data["transfer_to"] == data["transfer_from"]:
            raise serializers.ValidationError(f'Transfers cannot be made between two same accounts.')

        if not data["transfer_from"].is_active:
            raise serializers.ValidationError(f'Sending account must be active.')

        if not data["transfer_to"].is_active:
            raise serializers.ValidationError(f'Recipient account must be active')

        if data["transfer_from"].balance < data["amount"]:
            raise serializers.ValidationError(f'Insufficent Balance')

        return data


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = ('__all__')

    def validate(self, data):
        if not data["account"].is_active:
            raise serializers.ValidationError(f'Account is not active')

        if data["account"].balance < data["amount"]:
            raise serializers.ValidationError(f'Insufficent Balance')
        return data


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('__all__')

    def validate(self, data):
        if not data["account"].is_active:
            raise serializers.ValidationError(f'Account is not active')
        return data
