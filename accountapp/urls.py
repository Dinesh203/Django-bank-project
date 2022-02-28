from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('user_profile', views.user_profile, name="user_profile"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    path('account/', views.account, name="account"),
    path('withdraw/', views.withdraw, name="withdraw"),
    path('change_status/', views.change_status, name="change_status"),
    path('delete_account/<int:id>', views.delete_account, name="delete_account"),
    path('deposit/', views.deposit, name="deposit"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('send_money/', views.send_money, name="send_money"),
    path('tran_history/', views.transaction_history, name="transaction_history"),
    path('event_scheduler/', views.event_scheduler, name="event_scheduler"),


]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
