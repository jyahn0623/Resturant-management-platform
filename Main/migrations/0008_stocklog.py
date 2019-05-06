# Generated by Django 2.1.2 on 2019-05-06 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0007_auto_20190506_1439'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stocklog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sl_log', models.CharField(max_length=100, verbose_name='변경사항')),
                ('sl_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Main.Stock', verbose_name='재고명')),
            ],
        ),
    ]
