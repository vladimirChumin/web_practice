from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_alter_order_total_price"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CartItem",
        ),
        migrations.DeleteModel(
            name="Cart",
        ),
    ]

