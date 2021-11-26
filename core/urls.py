from django.urls import path
from . import views

#
urlpatterns = [
    path('', views.index, name="home_page"),
    # path('signup/', views.user_signup, name="signup_url"),

]