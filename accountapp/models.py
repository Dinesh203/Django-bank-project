from django.core.validators import MaxValueValidator
from django.db import models
import random
from django.contrib.auth.models import User

# Create your models here.


MALE = 'M'
FEMALE = 'F'
GENDER_CHOICE = (
    (MALE, "Male"),
    (FEMALE, "Female"),
)

SILVER = "S"
GOLD = "G"
PLATINUM = "P"
ACCOUNT_TYPE = (
    (SILVER, "SILVER"),
    (GOLD, "GOLD"),
    (PLATINUM, "PLATINUM")
)


class User_Model(models.Model):
    name = models.CharField(max_length=150, default="")
    email = models.EmailField(max_length=254, default="")
    password = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(decimal_places=2, max_digits=12)

    def __str__(self):
        return self.name


def random_string():
    """provide random account number
    """
    return str(random.randint(9000000000, 10000000000))


class UserBankAccount(models.Model):
    user = models.ForeignKey(User_Model, related_name='account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPE)
    account_no = models.PositiveIntegerField(unique=True, default=random_string())
    initial_balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    date_of_opening = models.DateField(auto_now_add=True, null=True)
    contact = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(9999999999)])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.account_no)


class MoneyTransfer(models.Model):
    """This model provide money transaction fields """
    owner = models.ForeignKey(User_Model, on_delete=models.CASCADE, blank=True, null=True)
    from_account = models.CharField(max_length=10)
    from_to = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    transaction_date = models.DateField(auto_now_add=True)
    remark = models.CharField(max_length=50, null=True)
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return str(self.amount)

# class UserBankAccountDetail(models.Model):
#     name = models.CharField(max_length=150)
#     contact = models.IntegerField(max_length=12)
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
#     birth_date = models.DateField(null=True, blank=True)
#     address = models.CharField(max_length=50, blank=True)
#     Initial_deposit = models.DecimalField(default=0, max_digits=12, decimal_places=2)
#     date_of_opening = models.DateField(auto_now_add=True)
#
#     def __str__(self):
#         return str(self.name)

# class Account(models.Model):
#     # Acc_type = models.ForeignKey(BankAccountType, on_delete=models.CASCADE)
#     user = models.OneToOneField(User, related_name="acccount", on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254, default="")
#     # gender = models.CharField(max_length=1, choices="GENDER_CHOICES")
#     address = models.CharField(max_length=50, blank=True)
#     # def __str__(self):
#     #     return self.name

# user = models.OneToOneField(User_Model, related_name='account', on_delete=models.CASCADE)
from django.db.models.fields import IntegerField