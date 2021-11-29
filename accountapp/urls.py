from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('transection/', views.transection, name="transection"),
  

]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
