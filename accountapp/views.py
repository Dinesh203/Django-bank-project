from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm, MoneyTransferForm
from .models import User_Model, UserBankAccount, BankAccountType
import decimal


# Create your views here.


def home(request):
    try:
        mail_id = request.session['email']
        user_id = User_Model.objects.get(email=mail_id)
        user_name = user_id.name
    except Exception as e:
        e = "Your session is expired please Login again"
        return render(request, 'accountapp/home.html', {'exception': e})
    return render(request, 'accountapp/home.html', {'user_name': user_name})
    

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
    if User_Model.objects.get(email=mail_id):
        mail_id = request.session['email']
        user_id = User_Model.objects.get(email=mail_id)
        user_name = user_id.name
        acc_type = BankAccountType.objects.all()
        for i in acc_type:
            type_name = i.name
            print(i.name)
        account_form = UserBankAccountForm()
        content = {'account_form': account_form,
                'user_detail': user_id
                }
        if request.method == "POST":
            account_type1 = request.POST['account_type']
            account_no1 = request.POST['account_no']
            initial_balance1 = request.POST['initial_balance']
            gender1 = request.POST['gender']
            birth_date1 = request.POST['birth_date']
            address1 = request.POST['address']
            obj = UserBankAccount.objects.create(user=user_id, account_type=type_name, account_no=account_no1,
                                                initial_balance=initial_balance1, gender=gender1,
                                                birth_date=birth_date1, address=address1)
            obj.save()
            messages.success(request, "Account added successfully!")
            return redirect('homepage')
        else:
            pass
        return render(request, "accountapp/create_acc.html", content)
    else:
        return HttpResponseRedirect("login", "Invalid Input login First")


def admin_login(request):
    if request.method == "POST":
        username = request.POST['Username']
        password1 = request.POST['password']
        if authenticate(username=username, password=password1):
            account_detail = UserBankAccount.objects.all()
            return render(request, "accountapp/admin_panel.html", {'account_detail': account_detail})
        else:
            msg = "Ty again, Fill correct Detail"
            return render(request, "accountapp/admin_access.html", {"msg": msg})
    else:
        admin = User.objects.all()
    return render(request, "accountapp/admin_access.html", {'admin': admin})



def logout(request):
    del request.session["email"]
    return render(request, 'base.html')


def transection(request):
    mail_id = request.session['email']
    user_id = User_Model.objects.get(email=mail_id)
    user_name = user_id.name
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            sender = UserBankAccount.objects.get(account_no=request.POST.get('send_from'))
            if sender.initial_balance > decimal.Decimal(request.POST.get('amount')):

                trans =  form.save()
                trans.owner = request.User_model.user
                trans.save()

                # debit the sender account
                sender.account_balance -= decimal.Decimal(request.POST.get('amount'))
                sender.save()

                #credit the receiver account
                receiver = UserBankAccount.objects.get(account_no=request.POST.get('send_to'))
                receiver.initial_balance += decimal.Decimal(request.POST.get('amount'))
                receiver.save()

                return redirect("homepage")
            # else:
            #     return 
    else:
        form = MoneyTransferForm()
        return render(request, "accountapp/transfer_money.html", {'form': form, 'user_name': user_name})




# , date_of_opening=date_of_opening1
# date_of_opening1 = request.POST['date_of_opening']


#
# def account(request):
#     mail_id = request.session['email']
#     user_id = User_Model.objects.get(email=mail_id)
#     user_name = user_id.name
#     print(user_id)
#     account_detail_form = UserBankAccountDetailForm()
#     content = {'account_detail_form': account_detail_form,
#                'user_detail': user_id
#                }
#     if request.method == "POST":
#         name1 = request.POST['name']
#         account_type1 = request.POST['account_type']
#         account_no1 = request.POST['account_no']
#         balance1 = request.POST['balance']
#         gender1 = request.POST['gender']
#         birth_date1 = request.POST['birth_date']
#         # date_of_opening1 = request.POST['date_of_opening']
#         # address1 = request.FILES['address']
#         obj = UserBankAccountDetail.objects.create(user=name1, account_type=account_type1, account_no=account_no1,
#                                                    balance=balance1,
#                                                    gender=gender1,
#                                                    birth_date=birth_date1)
#         obj.save()
#         messages.success(request, "Account added successfully!")
#         return redirect('home')
#     else:
#         pass
#     return render(request, "accountapp/create_acc.html", content)

#
