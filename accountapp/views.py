from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm, MoneyTransferForm
from .models import User_Model, UserBankAccount, BankAccountType, MoneyTransfer
import decimal


# Create your views here.
# def get_user_name(request):
#     mail_id = request.session['email']
#     user_id = User_Model.objects.get(email=mail_id)
#     user_name = user_id.name
#     print(user_name)
#     return user_name
#
# print(get_user_name(request))

def home(request):
    """" home page """
    if 'email' in request.session:
        mail_id = request.session['email']
        user_id = User_Model.objects.get(email=mail_id)
        user_name = user_id.name
        if UserBankAccount.objects.filter(user__email=mail_id).exists():
            account_detail = UserBankAccount.objects.get(user__email=mail_id)
            content = {
                'user_name': user_name,
                'account_detail': account_detail
            }
            return render(request, 'accountapp/home.html', content)
    else:
        e = "error occur!"
        return render(request, 'accountapp/home.html', {'exception': e})
    return render(request, 'accountapp/home.html')


def signup(request):
    """
    :return: Signup page and Create user basic detail.
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # msg = messages.success(request, 'Created User successfully!')
            return render(request, "accountapp/user_login.html")
    else:
        form = UserForm()
    return render(request, "accountapp/user_signup.html", {'form': form})


def login(request):
    """
    :return: login and authenticate User detail
    """
    if request.method == 'POST':
        email1 = request.POST['email']
        password1 = request.POST['password']
        if User_Model.objects.filter(email=email1, password=password1).exists():
            request.session['email'] = email1
            return redirect('homepage')
        else:
            msg = "invalid input please try again"
            return render(request, 'accountapp/user_login.html', {'msgs': msg})
    else:
        return render(request, 'accountapp/user_login.html')


def account(request):
    """
    This function help to Create an account.
    """
    mail_id = request.session['email']
    if User_Model.objects.get(email=mail_id):
        mail_id = request.session['email']
        user_id = User_Model.objects.get(email=mail_id)
        acc_type = BankAccountType.objects.all()
        for i in acc_type:
            type_name = i.name
        account_form = UserBankAccountForm()
        content = {'account_form': account_form,
                   'user_detail': user_id
                   }
        if request.method == "POST":
            account_no1 = request.POST['account_no']
            initial_balance1 = request.POST['initial_balance']
            gender1 = request.POST['gender']
            birth_date1 = request.POST['birth_date']
            address1 = request.POST['address']
            obj = UserBankAccount.objects.create(user=user_id, account_type=type_name, account_no=account_no1,
                                                 initial_balance=initial_balance1, gender=gender1,
                                                 birth_date=birth_date1, address=address1)
            obj.save()
            # messages.success(request, "Account added successfully!")
            return redirect('homepage')
        else:
            pass
        return render(request, "accountapp/create_acc.html", content)
    else:
        return HttpResponseRedirect("login", "Invalid Input login First")


def admin_login(request):
    """ This is super admin login page
    """
    if request.method == "POST":
        username = request.POST['Username']
        password1 = request.POST['password']
        if authenticate(username=username, password=password1):
            account_detail = UserBankAccount.objects.all()
            return render(request, "accountapp/admin_panel.html", {'account_detail': account_detail})
        else:
            msg = "Try again, Fill correct Detail"
            return render(request, "accountapp/admin_access.html", {"msg": msg})
    else:
        admin = User.objects.all()
    return render(request, "accountapp/admin_access.html", {'admin': admin})


def logout(request):
    """ This function helps to delete the Session.
    """
    del request.session["email"]
    return render(request, 'base.html')


def transaction(request):
    """
    Make a transaction, send Money to another account holder
    """
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            sender = UserBankAccount.objects.get(user__email=request.session['email'])
            
            print("sender", sender)
            if sender.initial_balance > decimal.Decimal(request.POST.get('amount')):
                sender.initial_balance -= decimal.Decimal(request.POST.get('amount'))

                # credit the receiver account
                receiver = UserBankAccount.objects.get(account_no=request.POST.get('from_to'))
                receiver.initial_balance += decimal.Decimal(request.POST.get('amount'))
                sender.save()
                receiver.save()

                # update form field from form data
                new_key = form.save()
                add_value = MoneyTransfer.objects.get(id=new_key.pk)
                add_value.from_account = sender.account_no
                add_value.opening_balance = decimal.Decimal(sender.initial_balance)

                # closing_bal.closing_balance = 423
                add_value.save()
                print(add_value.opening_balance)
                return redirect("homepage")
            else:
                message = "Insufficient Balance!"
                return render(request, "accountapp/transfer_money.html", {"message": message})
        else:
            messages.info(request, "Invalid Info please try again")
            return redirect("homepage")
    else:
        mail_id = request.session['email']
        user_id = User_Model.objects.get(email=mail_id)
        form = MoneyTransferForm()
        user_balance = UserBankAccount.objects.filter(user=user_id)
        for b in user_balance:
            print(b.initial_balance)
        content = {
            'form': form,
            'user_name': user_id.name,
            'balance': b.initial_balance
        }
        return render(request, "accountapp/transfer_money.html", content)


def transaction_history(request):
    """
    :return: View transaction history
    """
    mail_id = request.session['email']
    user_id = User_Model.objects.get(email=mail_id)
    statement_id = MoneyTransfer.objects.filter(owner__email=mail_id)
    balance_id = UserBankAccount.objects.filter(user__email=mail_id)
    for bal in balance_id:
        balance = bal.initial_balance
    for statement in statement_id:
        account_no = statement.from_account
    content = {
        'tran_id': statement_id,
        'owner_account_no': account_no,
        'user_name': user_id.name,
        'balance': balance,
        'balance_id': balance_id
    }
    return render(request, "accountapp/transactions.html", content)

#
# def show_balane(request):
#     mail_id = request.session['email']
#     user_id = User_Model.objects.get(email=mail_id)
#     user_bal = UserBankAccount.objects.get("initial_balance")
#     print(user_bal)
#     owner_balance = UserBankAccount.objects.get(initial_balance=UserBankAccount.objects.get(user=user_id))
#     print(owner_balance)


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


#
