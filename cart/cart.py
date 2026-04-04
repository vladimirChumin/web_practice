import json
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, Optional
from dataclasses import dataclass

from django.conf import settings

from bookshop.models import Book


@dataclass
class CartItem:
    book_id: int
    quantity: int

    @classmethod
    def from_raw(cls, book_id: str, raw: object) -> Optional["CartItem"]:
        """Поддерживаем 2 формата cookie:

        1) Новый (рекомендуемый): {"12": 2}
        2) Старый/совместимость: {"12": {"quantity": 2, "price": "..."}}

        Цена из cookie игнорируется.
        """
        if not str(book_id).isdigit():
            return None

        try:
            book_id_int = int(book_id)
        except (TypeError, ValueError):
            return None

        quantity_raw = None
        if isinstance(raw, int):
            quantity_raw = raw
        elif isinstance(raw, str) and raw.isdigit():
            quantity_raw = int(raw)
        elif isinstance(raw, dict):
            quantity_raw = raw.get("quantity")
        else:
            return None

        try:
            quantity_int = int(quantity_raw)
        except (TypeError, ValueError):
            return None

        if quantity_int <= 0:
            return None

        return cls(book_id=book_id_int, quantity=quantity_int)


class Cart:
    COOKIE_NAME = "cart"
    MAX_AGE = 60 * 60 * 24 * 30

    def __init__(self, request):
        self.request = request
        self._items: Dict[int, CartItem] = self._load_items()

    def _load_items(self) -> Dict[int, CartItem]:
        raw_cart = self.request.COOKIES.get(self.COOKIE_NAME, "{}")

        try:
            raw_data = json.loads(raw_cart)
        except json.JSONDecodeError:
            return {}

        if not isinstance(raw_data, dict):
            return {}

        items: Dict[int, CartItem] = {}
        for book_id, raw_item in raw_data.items():
            item = CartItem.from_raw(book_id, raw_item)
            if item:
                items[item.book_id] = item

        return items

    def get_quantity(self, book_id: int) -> int:
        item = self._items.get(book_id)
        return item.quantity if item else 0

    def set_qty(self, book_id: int, quantity: int) -> None:
        if quantity <= 0:
            self._items.pop(book_id, None)
            return

        self._items[book_id] = CartItem(book_id=book_id, quantity=quantity)

    def add_item(self, book_id: int, quantity: int = 1) -> None:
        if quantity <= 0:
            return

        current = self.get_quantity(book_id)
        self.set_qty(book_id, current + quantity)

    def remove_item(self, book_id: int) -> None:
        self._items.pop(book_id, None)

    def book_ids(self):
        return list(self._items.keys())

    def items(self):
        return list(self._items.values())

    def count(self) -> int:
        return sum(item.quantity for item in self._items.values())

    def clear(self) -> None:
        self._items = {}

    def to_dict(self) -> Dict[str, Any]:
        # Компактный формат cookie: {"12": 2}
        return {str(item.book_id): item.quantity for item in self._items.values()}

    def total_price(self) -> Decimal:
        books = Book.objects.filter(id__in=self.book_ids())
        price_by_id = {b.id: b.price for b in books}

        total = Decimal("0")
        for item in self._items.values():
            price = price_by_id.get(item.book_id)
            if price is None:
                continue
            try:
                total += Decimal(str(price)) * item.quantity
            except (InvalidOperation, TypeError):
                continue
        return total

    def save_to_response(self, response) -> None:
        response.set_cookie(
            self.COOKIE_NAME,
            json.dumps(self.to_dict(), separators=(",", ":")),
            max_age=self.MAX_AGE,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
        )

    def delete_from_response(self, response) -> None:
        response.delete_cookie(self.COOKIE_NAME)

