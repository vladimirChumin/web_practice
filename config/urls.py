from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("bookshop.urls")),
    path("account/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
]
