from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from bookshop.models import Book

SEED_BOOKS = [
    {"title": "Clean Code", "author": "Robert C. Martin", "price": Decimal("39.90"), "stock": 3},
    {"title": "The Pragmatic Programmer", "author": "Andrew Hunt", "price": Decimal("42.00"), "stock": 1},
    {"title": "Design Patterns", "author": "Erich Gamma", "price": Decimal("55.50"), "stock": 2},
    {"title": "You Don’t Know JS", "author": "Kyle Simpson", "price": Decimal("25.00"), "stock": 6},
    {"title": "Python Crash Course", "author": "Eric Matthes", "price": Decimal("30.00"), "stock": 1},
]

class Command(BaseCommand):
    help = "Seed initial books if Book table is empty (idempotent)."

    def handle(self, *args, **options):
        # если таблица существует, но данных нет — засеем
        if Book.objects.exists():
            self.stdout.write(self.style.SUCCESS("Books already exist — skipping seed."))
            return

        with transaction.atomic():
            Book.objects.bulk_create([Book(**b) for b in SEED_BOOKS])

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(SEED_BOOKS)} books."))
