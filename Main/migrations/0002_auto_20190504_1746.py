# Generated by Django 2.1.2 on 2019-05-04 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='o_status',
            field=models.BooleanField(default=False, verbose_name='상태'),
        ),
    ]
