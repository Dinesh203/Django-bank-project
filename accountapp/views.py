from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm
from .models import User_Model, UserBankAccount
from django.contrib.auth import authenticate, login


# Create your views here.
def home(request):
    form = UserForm()
    return render(request, 'accountapp/home.html',{'form': form})


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Created User successfully!')
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
            return redirect('homepage')
        else:
            msg = "invalid input please try again"
            return render(request, 'accountapp/user_login.html', {'mssg': msg})
    else:
        return render(request, 'accountapp/user_login.html')


def account(request):
    mail_id = request.session['email']
    user_id = User_Model.objects.get(email=mail_id)
    user_name = user_id.name
    account_form = UserBankAccountForm()
    content = {'account_form': account_form,
               'user_detail': user_id
               }
    if request.method == "POST":
        # user1 = request.POST['user']
        account_type1 = request.POST['account_type']
        account_no1 = request.POST['account_no']
        balance1 = request.POST['balance']
        gender1 = request.POST['gender']
        birth_date1 = request.POST['birth_date']
        date_of_opening1 = request.POST['date_of_opening']
        # address1 = request.FILES['address']
        obj = UserBankAccount.objects.create(user=user_name, account_type=account_type1, account_no=account_no1,
                                             balance=balance1,
                                             gender=gender1,
                                             birth_date=birth_date1, date_of_opening=date_of_opening1)
        obj.save()
        messages.success(request, "Account added successfully!")

        return redirect('home')
    else:
        account_form = UserBankAccount.objects.all()
        print(account_form)
    return render(request, "accountapp/create_acc.html", content)
