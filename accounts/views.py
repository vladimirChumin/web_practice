from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from .forms import RegisterUser
from django.shortcuts import redirect

class UserRegisterView(FormView):
    template_name = "personal_account/register.html"
    form_class = RegisterUser
    success_url = reverse_lazy("bookshop:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = "personal_account/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("bookshop:list")

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("bookshop:list")

