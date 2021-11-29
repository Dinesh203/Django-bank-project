from django.contrib import admin
from .models import BankAccountType, User_Model, UserBankAccount, MoneyTransfer

# Register your models here.


admin.site.register(BankAccountType)
admin.site.register(User_Model)
admin.site.register(UserBankAccount)
admin.site.register(MoneyTransfer)
