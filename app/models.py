from django.db import models
from datetime import datetime


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    identification_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return self.name

    def json_object(self):
        return {
            "name": self.name,
            "address": self.address,
            "identification_number": self.identification_number
        }


class Account(models.Model):
    """Bank Hesabı Oluşturulması"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    open_date = models.DateTimeField(null=True, blank=True)
    balance = models.FloatField()
    type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.open_date:
            self.open_date = datetime.now()
        super(Account, self).save(*args, **kwargs)

    def json_object(self):
        return {
            "open_date": self.open_date,
            "balance": self.balance,
            "customer": self.customer.id,
            "type": self.type
        }

    def __str__(self):
        return f"id:{self.id} - {self.customer.name}"


class Transfer(models.Model):
    amount = models.FloatField()
    transfer_from = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_from')
    transfer_to = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transfer_to')
    processing_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.processing_date:
            self.processing_date = datetime.now()
        super(Transfer, self).save(*args, **kwargs)

    def json_object(self):
        return {
            "amount": self.amount,
            "transfer_from": self.transfer_from,
            "transfer_to": self.transfer_to
        }

    def __str__(self):
        return f"{self.transfer_from.customer.name} - {self.transfer_to.customer.name} - Amount:{self.amount}"


class Deposit(models.Model):
    amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    processing_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.processing_date:
            self.processing_date = datetime.now()
        super(Deposit, self).save(*args, **kwargs)


class Withdraw(models.Model):
    amount = models.FloatField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    processing_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.processing_date:
            self.processing_date = datetime.now()
        super(Withdraw, self).save(*args, **kwargs)
