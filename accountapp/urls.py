from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),
    # path('services/', views.services, name="services"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('transaction/', views.transaction, name="transaction"),
    path('tran_history/', views.transaction_history, name="transaction_history"),


]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
