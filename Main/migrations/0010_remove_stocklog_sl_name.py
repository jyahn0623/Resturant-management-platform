# Generated by Django 2.1.2 on 2019-05-07 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0009_auto_20190506_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stocklog',
            name='sl_name',
        ),
    ]