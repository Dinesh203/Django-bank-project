from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('send_money/', views.send_money, name="send_money"),
    path('tran_history/', views.transaction_history, name="transaction_history"),


]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
