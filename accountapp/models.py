from django.db import models
import random
# from django.contrib.auth.models import AbstractUser
# from .managers import UserManager

# Create your models here.


MALE = 'M'
FEMALE = 'F'
GENDER_CHOICE = (
    (MALE, "Male"),
    (FEMALE, "Female"),
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

num = 9685452175
def random_string():
    return str(random.randint(9000000000, 10000000000))

    num += num+1


class UserBankAccount(models.Model):
    user = models.OneToOneField(User_Model, related_name='account', on_delete=models.CASCADE)
    account_type = models.ForeignKey(BankAccountType, related_name='accounts', on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField(unique=True, default=random_string())
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    date_of_opening = models.DateField(null=True, auto_now_add=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return str(self.account_no)

# class Account(models.Model):
#     # Acc_type = models.ForeignKey(BankAccountType, on_delete=models.CASCADE)
#     user = models.OneToOneField(User, related_name="acccount", on_delete=models.CASCADE)
#     email = models.EmailField(max_length=254, default="")
#     # gender = models.CharField(max_length=1, choices="GENDER_CHOICES")
#     address = models.CharField(max_length=50, blank=True)
#     # def __str__(self):
#     #     return self.name

    # user = models.OneToOneField(User_Model, related_name='account', on_delete=models.CASCADE)

