from django.db import models

class Book(models.Model):
    title = models.CharField("Название", max_length=256)
    author = models.CharField("Автор", max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(verbose_name="Осталось на складе")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.author} (Осталось: {self.stock})"

