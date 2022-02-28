from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm, UserBankAccountForm, MoneyTransferForm
from .models import User_Model, UserBankAccount, BankAccountType, MoneyTransfer
import decimal
from django.conf import settings
import socket
from ipware import get_client_ip
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
from datetime import datetime
import os
from pathlib import Path


def home(request):
    """" home page """
    if 'email' in request.session:
        mail_id = request.session['email']
        print(mail_id)
        user_id = User_Model.objects.filter(email=mail_id)
        for i in user_id:
            user_name = i.name
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


def signup(request, setting=None):
    """
    :return: Signup page and Create user basic detail.
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user_email = request.POST['email']
            print(user_email)
            send_mail("first mail", "this is email body", settings.EMAIL_HOST_USER, ['subham632541@gmail.com'],
                      fail_silently=False)
            print("send mail")

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
            user_name = user_id.name

            acc_type = BankAccountType.objects.all()
            for i in acc_type:
                type_name = i.name
            account_form = UserBankAccountForm()
            content = {'account_form': account_form,
                       'user_detail': user_id
                       }
            if request.method == "POST":
                account_no1 = request.POST['account_no']
                account_type1 = request.POST['account_type']
                initial_balance1 = request.POST['initial_balance']
                gender1 = request.POST['gender']
                contact1 = request.POST['contact']
                birth_date1 = request.POST['birth_date']
                address1 = request.POST['address']
                account_obj = UserBankAccount.objects.create(user=user_id, account_type=account_type1,
                                                             account_no=account_no1, initial_balance=initial_balance1,
                                                             gender=gender1, contact=contact1,
                                                             birth_date=birth_date1, address=address1)
                account_obj.save()
                return redirect('homepage')
            else:
                pass
            return render(request, "accountapp/create_acc.html", content)
        else:
            return HttpResponseRedirect("login", "Invalid Input login First")
    else:
        messages.success(request, 'Please Login To Enroll !')
        return redirect('login')


def event_scheduler(request):
    user = UserBankAccount.objects.get(user__email=request.session['email'])
    birth_date = user.birth_date
    print(birth_date)

    cal = Calendar()
    cal.add('attendee', 'MAILTO:abc@example.com')
    cal.add('attendee', 'MAILTO:xyz@example.com')

    event = Event()
    event.add('summary', 'Python meeting about calendaring')
    event.add('dtstart', datetime(2022, 10, 24, 8, 0, 0, tzinfo=pytz.utc))
    event.add('dtend', datetime(2022, 10, 24, 10, 0, 0, tzinfo=pytz.utc))
    event.add('dtstamp', datetime(2022, 10, 24, 0, 10, 0, tzinfo=pytz.utc))
    event.add('description', 'This is event description')

    organizer = vCalAddress('MAILTO:hello@example.com')
    organizer.params['cn'] = vText('Sir Jon')
    organizer.params['role'] = vText('CEO')
    event['organizer'] = organizer
    event['location'] = vText('London, UK')

    # Adding events to calendar
    cal.add_component(event)

    os.getcwd()
    directory = str(Path(__file__).parent.parent) + "/calender"
    print("ics file will be generated at ", directory)
    # os.mkdir(os.path.join(directory, "birth_date.ics"))
    f = open("birth_date.ics", "wb")
    f.write(cal.to_ical())
    f.close()

    return redirect('homepage')


def user_profile(request):
    """ This function helps to user can view profile and update.
    """
    # hostname = socket.gethostname()
    # IPAddr = socket.gethostbyname(hostname)
    # print("Your Computer Name is:" + hostname)
    # print("Your Computer IP Address is:" + IPAddr)
    ip, is_routable = get_client_ip(request)
    if ip is None:
        print("ip is none ", ip)
    # Unable to get the client's IP address
    else:

        # We got the client's IP address
        if is_routable:
            print("is routable", is_routable)
        # The client's IP address is publicly routable on the Internet
        else:
            print("ip is private address")
    # The client's IP address is private

    # Order of precedence is (Public, Private, Loopback, None)
    print(get_client_ip(request))

    if "email" in request.session:
        if UserBankAccount.objects.get(user__email=request.session['email']):
            profile = UserBankAccount.objects.get(user__email=request.session['email'])
            return render(request, 'accountapp/user_profile.html', {"profile": profile})
    else:
        return redirect("login")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def change_status(request):
    """ user can change account status like active/deactivate.
    """
    change = UserBankAccount.objects.get(user__email=request.session['email'])
    if change.status:
        change.status = False
        change.save()
    else:
        change.status = True
        change.save()
    return redirect('homepage')


def delete_account(request, id):
    """ Delete Account
    """
    print(id)
    # account_detail = UserBankAccount.objects.get(user_id=id)
    # print(account_detail)
    delete = UserBankAccount.objects.get(user_id=id)
    delete.delete()
    return redirect('login')


def admin_login(request):
    """ This is super admin login page
    """
    if request.method == "POST":
        username = request.POST['Username']
        password1 = request.POST['password']
        if authenticate(username=username, password=password1):
            account_detail = UserBankAccount.objects.all()
            user_detail = User_Model.objects.all()
            context = {
                "account_detail": account_detail,
                "user_detail": user_detail
            }
            return render(request, "accountapp/admin_panel.html", context)
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
    check_status = UserBankAccount.objects.get(user__email=request.session['email'])
    if check_status.status:
        if request.method == 'POST':
            form = MoneyTransferForm(request.POST)
            if form.is_valid():
                sender = UserBankAccount.objects.get(user__email=request.session['email'])

                # debit amount from sender account
                if sender.account_no != request.POST.get('to_account'):
                    if sender.initial_balance > decimal.Decimal(request.POST.get('amount')):
                        sender.initial_balance -= decimal.Decimal(request.POST.get('amount'))

                        # update form field from form data
                        new_key = form.save()
                        add_value = MoneyTransfer.objects.get(id=new_key.pk)
                        add_value.from_account = sender.account_no
                        add_value.transaction_mode = "send-money"
                        add_value.owner = sender.user
                        add_value.deposit_amount = decimal.Decimal(0)
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
                    message = "Insufficient Balance! or Invalid Detail!"
                    return render(request, "accountapp/transfer_money.html", {"message": message})
            else:
                messages.info(request, "Invalid Info please try again")
                return redirect("homepage")
        else:
            user_id = User_Model.objects.filter(email=request.session['email'])
            user_name = [i.name for i in user_id]
            user_balance = UserBankAccount.objects.filter(user__email=request.session['email'])
            initial_bal = [j.initial_balance for j in user_balance]
            form = MoneyTransferForm()
            context = {
                'form': form,
                'user_name': user_name,
                'balance': initial_bal
            }
            return render(request, "accountapp/transfer_money.html", context)
    else:
        message = "exception"
        return render(request, 'accountapp/home.html', {'message': message})


def transaction_history(request):
    """
    :return: View transaction history
    """
    account_detail = UserBankAccount.objects.filter(user__email=request.session['email'])
    for detail in account_detail:
        balance = detail.initial_balance
        user_name = detail.user
        account_no = detail.account_no
    statement_id = MoneyTransfer.objects.filter(owner__email=request.session['email'])
    for statement in statement_id:
        print(statement.opening_balance)
    content = {
        'tran_id': statement_id,
        'detail': detail,
        'user_name': user_name,
        'balance': balance,
    }
    return render(request, "accountapp/transactions.html", content)


def withdraw(request):
    """ withdrawal money
    """
    check_status = UserBankAccount.objects.get(user__email=request.session['email'])
    if check_status.status:
        if request.method == 'POST':
            amount1 = request.POST['amount']
            withdrawal = UserBankAccount.objects.get(user__email=request.session['email'])
            if withdrawal.initial_balance > decimal.Decimal(amount1):
                withdrawal.initial_balance -= decimal.Decimal(amount1)
                withdrawal.save()
                opening_balance1 = withdrawal.initial_balance
                user1 = withdrawal.user
                from_account1 = withdrawal.account_no
                amount_placeholder = decimal.Decimal(0)
                transaction_mode1 = 'self-withdrawal'
                withdraw_form = MoneyTransfer.objects.create(owner=user1, from_account=from_account1, amount=amount1,
                                                             transaction_mode=transaction_mode1,
                                                             deposit_amount=amount_placeholder,
                                                             opening_balance=opening_balance1)
                withdraw_form.save()
                print(withdraw_form.opening_balance)
                return redirect('homepage')
            else:
                message = "Transaction Failed!, may be have insufficient balance"
                return render(request, 'accountapp/withdraw_money.html', {'message': message})
        # else:
        account_detail = UserBankAccount.objects.filter(user__email=request.session['email'])
        for i in account_detail:
            balance = i.initial_balance
            print(balance)
        return render(request, 'accountapp/withdraw_money.html', {'account_detail': account_detail})
    else:
        exception = "e"
        return render(request, 'accountapp/withdraw_money.html', {'exception': exception})


def deposit(request):
    """ Deposit money
    """
    check_status = UserBankAccount.objects.get(user__email=request.session['email'])
    if check_status.status:
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
            depositor_form = MoneyTransfer.objects.create(owner=user1, from_account=from_account1,
                                                          amount=amount_placeholder,
                                                          deposit_amount=amount1, transaction_mode=transaction_mode1,
                                                          opening_balance=opening_balance1)
            depositor_form.save()
            print(depositor_form.opening_balance)
            return redirect('homepage')

        account_detail = UserBankAccount.objects.filter(user__email=request.session['email'])
        return render(request, 'accountapp/deposit_money.html', {'account_detail': account_detail})
    else:
        exception = "e"
        return render(request, 'accountapp/deposit_money.html', {'exception': exception})
