from django.urls import path

from .views import login, logout, signup

urlpatterns = [
    path("signup/", signup),
    path("login/", login),
    path("logout/", logout),
]
