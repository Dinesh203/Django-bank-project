from django.urls import path
from . import views

#
urlpatterns = [
    path('', views.user_signup, name="user_signup"),
    # path('signup/', views.user_signup, name="signup_url"),

]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
