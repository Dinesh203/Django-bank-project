from django.contrib.auth import authenticate
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm, MoneyTransferForm
from .models import User_Model, UserBankAccount, BankAccountType, MoneyTransfer
import decimal


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
    if 'email' in request.session:
        if User_Model.objects.get(email=request.session['email']):
            user_id = User_Model.objects.get(email=request.session['email'])
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
                account_obj = UserBankAccount.objects.create(user=user_id, account_type=type_name, account_no=account_no1,
                                                    initial_balance=initial_balance1, gender=gender1,
                                                    birth_date=birth_date1, address=address1)
                account_obj.save()
                # messages.success(request, "Account added successfully!")
                return redirect('homepage')
            else:
                pass
            return render(request, "accountapp/create_acc.html", content)
        else:
            return HttpResponseRedirect("login", "Invalid Input login First")
    else:
        messages.success(request,'Please Login To Enroll !')
        return redirect('login')


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


def send_money(request):
    """
    Make a transaction, send Money to another account holder.
    """
    if request.method == 'POST':
        form = MoneyTransferForm(request.POST)
        if form.is_valid():
            sender = UserBankAccount.objects.get(user__email=request.session['email'])

            # debit amount from sender account
            if sender.initial_balance > decimal.Decimal(request.POST.get('amount')):
                sender.initial_balance -= decimal.Decimal(request.POST.get('amount'))

                # update form field from form data
                new_key = form.save()
                add_value = MoneyTransfer.objects.get(id=new_key.pk)
                add_value.from_account = sender.account_no
                add_value.transaction_mode = "send-money"
                add_value.owner = sender.user
                add_value.opening_balance = decimal.Decimal(sender.initial_balance)

                # credit amount from receiver account
                receiver = UserBankAccount.objects.get(account_no=request.POST.get('to_account'))
                receiver.initial_balance += decimal.Decimal(request.POST.get('amount'))
                sender.save()
                receiver.save()

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
    account_detail = UserBankAccount.objects.filter(user__email=request.session['email'])
    for detail in account_detail:
        balance = detail.initial_balance
        user_name = detail.user

    statement_id = MoneyTransfer.objects.filter(owner__email=request.session['email'])
    for statement in statement_id:
        print(statement.opening_balance)
    content = {
        'tran_id': statement_id,
        'statement': statement,
        'user_name': user_name,
        'balance': balance,
    }
    return render(request, "accountapp/transactions.html", content)


def withdraw(request):
    """ withdrawal money
    """
    if request.method == 'POST':
        amount1 = request.POST['amount']
        withdrawal = UserBankAccount.objects.get(user__email=request.session['email'])
        if withdrawal.initial_balance > decimal.Decimal(amount1):
            withdrawal.initial_balance -= decimal.Decimal(amount1)
            withdrawal.save()
            opening_balance1 = withdrawal.initial_balance
            user1 = withdrawal.user
            from_account1 = withdrawal.account_no
            transaction_mode1 = 'self-withdrawal'
            withdraw_form = MoneyTransfer.objects.create(owner=user1, from_account=from_account1, amount=amount1,
                                                         transaction_mode=transaction_mode1,
                                                         opening_balance=opening_balance1)
            withdraw_form.save()
            print(withdraw_form.opening_balance)
            return redirect('homepage')
        else:
            message = "Transaction Failed!, may be have insufficient balance"
            return render(request, 'accountapp/withdraw_money.html', {'message': message})
    # else:
    #
    return render(request, 'accountapp/withdraw_money.html')

    

def deposit(request):
    """ Deposit money
    """
    if request.method == 'POST':
        amount1 = request.POST['deposit_amount']
        depositor = UserBankAccount.objects.get(user__email=request.session['email'])
        depositor.initial_balance += decimal.Decimal(amount1)
        depositor.save()
        user1 = depositor.user
        from_account1 = depositor.account_no
        amount_placeholder = decimal.Decimal(0)
        transaction_mode1 = 'deposit-money'
        opening_balance1 = depositor.initial_balance
        depositor_form = MoneyTransfer.objects.create(owner=user1, from_account=from_account1, amount=amount_placeholder,
                                                        deposit_amount=amount1, transaction_mode=transaction_mode1,
                                                        opening_balance=opening_balance1)
        depositor_form.save()
        print(depositor_form.opening_balance)
        return redirect('homepage')
        # else:
        #     message = "Transaction Failed!, may be have insufficient balance"
        #     return render(request, 'accountapp/deposit_money.html', {'message': message})
    # else:
    #
    return render(request, 'accountapp/deposit_money.html')