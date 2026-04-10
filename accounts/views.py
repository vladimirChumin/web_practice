from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView, UpdateView
from .forms import RegisterUser, ProfileUpdateForm
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.db import connection
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

from .forms import UnsafeUserSearchForm


from .mixin import LoginRequiredMixin

user = get_user_model()

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
    


class UnsafeUserSearchView(View):
    template_name = "personal_account/search_form.html"

    def get(self, request):
        form = UnsafeUserSearchForm(request.GET or None)
        rows = []
        error = None

        if form.is_valid():
            username = form.cleaned_data["username"]

            sql = (
                "SELECT username, email "
                f"FROM auth_user "
                f"WHERE username = '{username}'"
            )

            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
            except Exception as e:
                error = str(e)

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "rows": rows,
                "error": error,
            },
        )

class CheckUniqueView(View):
    def get(self, request):
        field = request.GET.get("field")
        value = (request.GET.get("value") or "").strip()

        if field not in {"username", "email"}:
            return JsonResponse({"ok": False, "error": "invalid_field"}, status=400)

        if not value:
            return JsonResponse({"ok": False, "available": False, "error": "empty"}, status=400)

        lookup = {f"{field}__iexact": value}
        exists = user.objects.filter(**lookup).exists()

        return JsonResponse({"ok": True, "available": not exists})
