from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = "bookshop/book_list.html"
    context_object_name = "books"
    paginate_by = 5
    ordering = ["id"]

class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "price", "stock"]
    template_name = "bookshop/book_form.html"
    success_url = reverse_lazy("bookshop:list")

class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "author", "price", "stock"]
    template_name = "bookshop/book_form.html"
    success_url = reverse_lazy("bookshop:list")

class BookDeleteView(DeleteView):
    model = Book
    template_name = "bookshop/book_confirm_delete.html"
    success_url = reverse_lazy("bookshop:list")