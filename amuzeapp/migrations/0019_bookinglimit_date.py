# Generated by Django 4.1.7 on 2023-04-02 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0018_alter_predict_count_child'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinglimit',
            name='date',
            field=models.DateField(null=True, unique=True),
        ),
    ]
