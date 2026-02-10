from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book
from accounts.mixin import AdminRequiredMixin, LoginRequiredMixin

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


