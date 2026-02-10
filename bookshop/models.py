from django.db import models
from django.conf import settings

class Book(models.Model):
    title = models.CharField("Название", max_length=256)
    author = models.CharField("Автор", max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name="Осталось на складе")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author} (Осталось: {self.stock})"

class Profile(models.Model):
    class Role(models.TextChoices):
        USER = "user", "Обычный пользователь"
        ADMIN = "admin", "Администратор"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name="profile"
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
