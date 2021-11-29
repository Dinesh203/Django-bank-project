from django import forms
from .models import User_Model, UserBankAccount
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
