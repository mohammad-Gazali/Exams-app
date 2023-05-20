from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginCustomForm
from . import views


urlpatterns = [
    # normal views urls
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", views.register, name="sign_up"),
    path("login", LoginView.as_view(authentication_form=LoginCustomForm), name="login"),
]
