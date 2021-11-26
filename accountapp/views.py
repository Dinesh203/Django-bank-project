from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import HttpResponse
# from adminapp.models import Post
# from .forms import SignUpForm
from django.contrib.auth.models import User
from .forms import UserSignUpForm
from django.contrib.auth import authenticate

# Create your views here.


# def index(request):
#     """ this is banking Home page
#     :return: home page
#     """
#     return render(request, "accountapp/home.html")


def user_signup(request):
    if request.method == "POST":
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            message = messages.success(request, 'Created User successfully')
            return redirect("login")
    else:
        user_Profile = UserSignUpForm()
    return render(request, "accountapp/home.html", {'user': user_Profile})

