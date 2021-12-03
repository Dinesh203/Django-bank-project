from django import forms
from .models import User_Model, UserBankAccount, MoneyTransfer
from django.forms.widgets import NumberInput
from django.forms import ModelForm


# from .views import get_user_name


class UserForm(forms.ModelForm):
    """
    :return: User Form Detail
    """
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User_Model
        fields = "__all__"


class UserBankAccountForm(forms.ModelForm):
    """
    :return: User account form detail
    """
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    class Meta:
        model = UserBankAccount
        fields = "__all__"


class MoneyTransferForm(forms.ModelForm):
    # owner = forms.CharField(disabled=True, widget=forms.HiddenInput(), show_hidden_initial="hello")

    class Meta:
        model = MoneyTransfer
        fields = ['to_account', 'amount', 'remark']
        # exclude = ('owner',)



# ,  UserBankAccountDetail
# user = forms.CharField(widget=forms.HiddenInput(), initial=get_user_name())
