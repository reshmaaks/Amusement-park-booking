# Generated by Django 4.1.7 on 2023-03-17 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amuzeapp', '0008_merge_0007_book_0007_booking'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payments',
            old_name='order_id',
            new_name='razorpay_order_id',
        ),
        migrations.AddField(
            model_name='payments',
            name='razorpay_payment_status',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='payments',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='booking',
        ),
    ]