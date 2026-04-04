from bookshop.models import Book

from .cart import Cart


def add_to_cart(request, book_id: int, qty: int = 1):
    cart = Cart(request)
    book = Book.objects.get(id=book_id)

    new_quantity = cart.get_quantity(book_id) + qty
    if new_quantity > book.stock:
        return False, cart

    cart.set_qty(book_id, new_quantity)
    return True, cart
