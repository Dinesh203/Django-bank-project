from django import forms
from .models import User_Model, UserBankAccount, MoneyTransfer
from django.forms import ModelForm


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User_Model
        fields = "__all__"


class UserBankAccountForm(forms.ModelForm):

    class Meta:
        model = UserBankAccount
        fields = "__all__"


class MoneyTransferForm(forms.ModelForm):

    class Meta:
        model = MoneyTransfer
        fields = "__all__"

        
#
# class UserBankAccountDetailForm(forms.ModelForm):
#     class Meta:
#         model = UserBankAccountDetail
#         fields = "__all__"

# ,  UserBankAccountDetail