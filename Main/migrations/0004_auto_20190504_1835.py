# Generated by Django 2.1.2 on 2019-05-04 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0003_auto_20190504_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='s_status',
            field=models.BooleanField(default=True, verbose_name='상태'),
        ),
    ]
