from django.urls import path
from . import views
from django.urls import include
# urls

urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("account/<str:type>", views.account, name="account"),
    # path("accounts/", include("django.contrib.auth.urls"))
    path("assignments", views.assignments, name="assignments"),
    path("assignments/a/<str:type>", views.a, name='a')
]
