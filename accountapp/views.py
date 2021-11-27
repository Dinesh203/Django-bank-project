from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm
from .models import User_Model, UserBankAccount
from django.contrib.auth import authenticate, login


# Create your views here.
def home(request):
    return render(request, 'core/base.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Created User successfully')
            return render(request, "accountapp/user_login.html")
    else:
        form = UserForm()
    return render(request, "accountapp/user_signup.html", {'form': form})


def login(request):
    if request.method == 'POST':
        email1 = request.POST['email']
        password1 = request.POST['password']
        if User_Model.objects.filter(email=email1, password=password1).exists():
            request.session['email'] = email1
            return redirect("account")
        else:
            msg = "invalid input please try again"
            return render(request, 'accountapp/user_login.html', {'mssg': msg})
    else:
        return render(request, 'accountapp/user_login.html')


def account(request):
    mail_id = request.session['email']
    user_id = User_Model.objects.get(email=mail_id)
    account_form = UserBankAccountForm()
    content = {'account_form': account_form,
               'user_detail': user_id
               }
    if request.method == "POST":
        user1 = request.POST['user']
        account_type1 = request.POST['account_type']
        account_no1 = request.POST['account_no']
        balance1 = request.POST['balance']
        initial_deposit_date1 = request.POST['initial_deposit_date']
        gender1 = request.POST['gender']
        birth_date1 = request.POST['birth_date']
        # address1 = request.FILES['address']
        obj = UserBankAccount.objects.create(user=user1, account_type=account_type1, account_no=account_no1,
                                             balance=balance1,
                                             initial_deposit_date=initial_deposit_date1, gender=gender1,
                                             birth_date=birth_date1)
        obj.save()
        messages.success(request, "Account added successfully!")

        return redirect('home')
    else:
        account_form = UserBankAccountForm()
    return render(request, "accountapp/create_acc.html", content)
