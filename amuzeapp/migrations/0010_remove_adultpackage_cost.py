# Generated by Django 4.1.7 on 2023-03-30 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0009_predict_delete_prediction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adultpackage',
            name='cost',
        ),
    ]
