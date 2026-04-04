from django.urls import path
from .views import *
from django.views.generic import TemplateView


app_name = "accounts"

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("settings/", SettingsView.as_view(), name="settings"),
    path("profile/", TemplateView.as_view(template_name="personal_account/profile.html"), name="profile"),

]