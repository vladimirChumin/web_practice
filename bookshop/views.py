from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book
from django.views.generic import FormView
from .forms import RegisterUser
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from .mixin import AdminRequiredMixin, LoginRequiredMixin

class BookListView(ListView):
    model = Book
    template_name = "bookshop/book_list.html"
    context_object_name = "books"
    paginate_by = 50
    ordering = ["id"]

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ["title", "author", "price", "stock"]
    template_name = "bookshop/book_form.html"
    success_url = reverse_lazy("bookshop:list")

class BookUpdateView(AdminRequiredMixin, UpdateView):
    model = Book
    fields = ["title", "author", "price", "stock"]
    template_name = "bookshop/book_form.html"
    success_url = reverse_lazy("bookshop:list")

class BookDeleteView(AdminRequiredMixin, DeleteView):
    model = Book
    template_name = "bookshop/book_confirm_delete.html"
    success_url = reverse_lazy("bookshop:list")

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

