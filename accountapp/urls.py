from django.urls import path
from . import views

#
urlpatterns = [
    path('', views.home, name="homepage"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('account/', views.account, name="account"),
    path('admin_login/', views.admin_login, name="admin_login"),
    # path('admin_panel/', views.admin_panel, name="admin_panel"),

]


# path('changestatus/<id>', views.changestatus, name="changestatus"),
