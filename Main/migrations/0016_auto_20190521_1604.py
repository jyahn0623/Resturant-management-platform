# Generated by Django 2.2 on 2019-05-21 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0015_order_sheet_table_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_order',
            name='to_order_date',
        ),
        migrations.AddField(
            model_name='order_sheet',
            name='os_order_date',
            field=models.DateTimeField(auto_now=True, verbose_name='주문 시간'),
        ),
    ]
