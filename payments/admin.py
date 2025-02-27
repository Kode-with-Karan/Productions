from django.contrib import admin
from .models import Transaction, Earnings, WithdrawalRequest

# Register your models here.

admin.site.register(Transaction)
admin.site.register(Earnings)
admin.site.register(WithdrawalRequest)
