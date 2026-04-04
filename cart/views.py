from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.db import transaction

from .models import OrderItem, Order
from bookshop.models import Book

from .cart import Cart
from .services import add_to_cart


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, book_id: int):
        book = Book.objects.get(id=book_id)

        if book.stock <= 0:
            messages.error(request, "Книга закончилась на складе.")
            return redirect(request.POST.get("next", reverse("bookshop:list")))

        success, cart = add_to_cart(request, book_id)
        if not success:
            messages.error(request, "Недостаточно книг на складе.")
            response = redirect(request.POST.get("next", reverse("bookshop:list")))
            cart.save_to_response(response)
            return response

        messages.success(request, "Книга добавлена в корзину.")
        response = redirect(request.POST.get("next", reverse("bookshop:list")))
        cart.save_to_response(response)
        return response


class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        books = Book.objects.in_bulk(cart.book_ids())

        items = []
        total = 0
        for it in cart.items():
            book = books.get(it.book_id)
            if not book:
                continue
            row_total = book.price * it.quantity
            total += row_total
            items.append({"book": book, "quantity": it.quantity, "row_total": row_total})

        return render(request, "cart/cart.html", {"items": items, "total": total})


class RemoveFromCartView(LoginRequiredMixin, View):
    def post(self, request, book_id: int):
        cart = Cart(request)
        cart.remove_item(book_id)
        response = redirect("cart:view")
        cart.save_to_response(response)
        return response


class SetQtyView(LoginRequiredMixin, View):
    def post(self, request, book_id: int):
        quantity = int(request.POST.get("quantity", 1))
        book = get_object_or_404(Book, id=book_id)

        cart = Cart(request)

        if quantity < 1:
            cart.remove_item(book_id)
            messages.warning(request, "Товар удален из корзины.")
            response = redirect("cart:view")
            cart.save_to_response(response)
            return response

        if quantity > book.stock:
            messages.error(request, "Недостаточно книг на складе.")
        else:
            cart.set_qty(book_id, quantity)
            messages.success(request, "Количество обновлено.")

        response = redirect("cart:view")
        cart.save_to_response(response)
        return response


class CheckoutView(LoginRequiredMixin, View):
    @transaction.atomic
    def post(self, request):
        cart = Cart(request)

        if not cart.items():
            messages.error(request, "Корзина пуста.")
            return redirect("cart:view")

        books = Book.objects.select_for_update().in_bulk(cart.book_ids())

        for it in cart.items():
            book = books.get(it.book_id)
            if not book:
                messages.error(request, "Одна из книг больше недоступна.")
                return redirect("cart:view")
            if it.quantity > book.stock:
                messages.error(request, f"Недостаточно книг '{book.title}' на складе.")
                return redirect("cart:view")

        cur_order = Order.objects.create(user=request.user)
        for it in cart.items():
            book = books[it.book_id]
            book.stock -= it.quantity
            book.save()

            OrderItem.objects.create(
                order=cur_order,
                book=book,
                quantity=it.quantity,
                price=book.price,
            )

        cur_order.total_price = cur_order.get_price()
        cur_order.save()

        cart.clear()
        messages.success(request, "Заказ оформлен успешно!")
        response = redirect("cart:view")
        cart.delete_from_response(response)
        return response


class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "cart/orders_list.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by("-created_at")
