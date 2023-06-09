# Generated by Django 4.1.7 on 2023-03-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0008_prediction'),
    ]

    operations = [
        migrations.CreateModel(
            name='predict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=20)),
                ('count_adult', models.BigIntegerField(default=1)),
                ('count_child', models.BigIntegerField(default=1)),
                ('offers', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='prediction',
        ),
    ]
