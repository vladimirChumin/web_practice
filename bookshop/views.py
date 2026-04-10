from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book
from accounts.mixin import AdminRequiredMixin, LoginRequiredMixin

class BookListView(ListView):
    model = Book
    template_name = "bookshop/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    ordering = ["id"]

    def get_queryset(self):
        qs = super().get_queryset()

        author = (self.request.GET.get("author") or "").strip()
        if author:
            qs = qs.filter(author__icontains=author)

        in_stock = self.request.GET.get("in_stock")
        if in_stock in {"1", "true", "on", "yes"}:
            qs = qs.filter(stock__gt=0)

        return qs

    def get_paginate_by(self, queryset):
        try:
            per = int(self.request.GET.get("per", self.paginate_by))
            return max(1, per)
        except ValueError:
            return self.paginate_by


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
