from django.urls import path
from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView, UserRegisterView, UserLoginView, UserLogoutView


app_name = "bookshop"

urlpatterns = [
    path("", BookListView.as_view(), name="list"),
    path("create/", BookCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", BookUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", BookDeleteView.as_view(), name="delete"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout")
]

