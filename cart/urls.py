from django.urls import path
from .views import *

app_name = "cart"

urlpatterns = [
    path("add/<int:book_id>/", AddToCartView.as_view(), name="add"),
    path("orders/", CartView.as_view(), name="view"),
    path("set/<int:book_id>/", SetQtyView.as_view(), name="set_qty"),
    path("remove/<int:book_id>/", RemoveFromCartView.as_view(), name="remove"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("orders_list", OrdersListView.as_view(), name="orders_list"),
]
