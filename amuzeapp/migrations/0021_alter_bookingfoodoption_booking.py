# Generated by Django 4.1.7 on 2023-04-12 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0020_remove_product_brand_delete_fooditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingfoodoption',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amuzeapp.placed_booking'),
        ),
    ]
