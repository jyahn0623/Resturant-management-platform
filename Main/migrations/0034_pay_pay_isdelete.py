# Generated by Django 2.2.1 on 2019-05-25 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0033_auto_20190526_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='pay_isdelete',
            field=models.BooleanField(default=False, verbose_name='삭제'),
        ),
    ]
