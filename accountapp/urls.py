from django.urls import path
from . import views

#
urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('account/', views.account, name="account"),

]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
