from django.db import models
from django.conf import settings

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

