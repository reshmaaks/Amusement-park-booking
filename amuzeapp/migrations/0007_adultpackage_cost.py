# Generated by Django 4.1.7 on 2023-03-28 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0006_bookinglimit'),
    ]

    operations = [
        migrations.AddField(
            model_name='adultpackage',
            name='cost',
            field=models.BigIntegerField(default=0, null=True),
        ),
    ]
