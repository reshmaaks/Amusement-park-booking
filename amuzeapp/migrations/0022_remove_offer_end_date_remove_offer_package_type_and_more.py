# Generated by Django 4.1.7 on 2023-03-24 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0021_offer_end_date_offer_package_type_offer_start_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='package_type',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='start_date',
        ),
        migrations.AddField(
            model_name='offer',
            name='count_adult',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='count_child',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
