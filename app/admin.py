from django.contrib import admin
from app.models import (Customer,Account,Transfer,Withdraw,Deposit)

admin.site.register(Customer)
admin.site.register(Account)
admin.site.register(Transfer)
admin.site.register(Withdraw)
admin.site.register(Deposit)