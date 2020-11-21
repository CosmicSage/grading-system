from django.urls import path
from . import views

# urls
urlpatterns = [
    path("", views.index, name="home"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("register", views.register, name="register"),
    path("account/<str:type>", views.account, name="account"),
]
