# Generated by Django 4.1.7 on 2023-04-01 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0016_placed_booking_food'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='amuzeapp.book'),
        ),
    ]
