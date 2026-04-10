from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookListFilterTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Book.objects.create(title="Война и мир", author="Лев Толстой", price="100.00", stock=3)
        Book.objects.create(title="Анна Каренина", author="Лев Толстой", price="120.00", stock=0)
        Book.objects.create(title="Преступление и наказание", author="Достоевский", price="90.00", stock=5)

    def test_filter_by_author_icontains(self):
        url = reverse("bookshop:list")
        resp = self.client.get(url, {"author": "толстой"})
        self.assertEqual(resp.status_code, 200)
        books = list(resp.context["books"])
        self.assertEqual({b.title for b in books}, {"Война и мир", "Анна Каренина"})

    def test_filter_in_stock_only(self):
        url = reverse("bookshop:list")
        resp = self.client.get(url, {"in_stock": "1"})
        self.assertEqual(resp.status_code, 200)
        books = list(resp.context["books"])
        self.assertEqual({b.title for b in books}, {"Война и мир", "Преступление и наказание"})

    def test_filter_author_and_in_stock_combined(self):
        url = reverse("bookshop:list")
        resp = self.client.get(url, {"author": "толстой", "in_stock": "1"})
        self.assertEqual(resp.status_code, 200)
        books = list(resp.context["books"])
        self.assertEqual([b.title for b in books], ["Война и мир"])
