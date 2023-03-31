# Generated by Django 4.1.7 on 2023-03-25 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0005_book_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingLimit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_bookings', models.PositiveIntegerField(default=True)),
            ],
        ),
    ]