# Generated by Django 2.2.1 on 2019-05-25 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0028_auto_20190526_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='end_day_work',
        ),
        migrations.RemoveField(
            model_name='work',
            name='night_work',
        ),
        migrations.RemoveField(
            model_name='work',
            name='start_day_work',
        ),
        migrations.RemoveField(
            model_name='work',
            name='total_work',
        ),
        migrations.AddField(
            model_name='work',
            name='day_work',
            field=models.DateTimeField(blank=True, null=True, verbose_name='근무일'),
        ),
        migrations.AlterField(
            model_name='work',
            name='daytime_work',
            field=models.IntegerField(blank=True, null=True, verbose_name='근무시간'),
        ),
    ]
