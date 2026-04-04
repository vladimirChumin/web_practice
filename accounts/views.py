from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, UpdateView
from .forms import RegisterUser, ProfileUpdateForm
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash



from .mixin import LoginRequiredMixin

user = get_user_model()

class UserRegisterView(FormView):
    template_name = "personal_account/settings.html"
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

class SettingsView(LoginRequiredMixin, UpdateView):
    model = user
    form_class = ProfileUpdateForm
    template_name = "personal_account/settings.html"
    success_url = reverse_lazy("accounts:settings")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        if form.cleaned_data.get("password1"):
            update_session_auth_hash(self.request, self.object)
        return response