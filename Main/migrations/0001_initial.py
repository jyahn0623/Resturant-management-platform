# Generated by Django 2.1.2 on 2019-05-04 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_name', models.CharField(max_length=30)),
                ('o_count', models.PositiveIntegerField()),
                ('o_order_at', models.DateTimeField(verbose_name='주문일자')),
                ('o_status', models.BooleanField(verbose_name='상태')),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=30)),
                ('s_incoming_at', models.DateField(verbose_name='반입일자')),
                ('s_status', models.BooleanField(verbose_name='상태')),
                ('s_caution_num', models.PositiveIntegerField()),
                ('s_expire_at', models.DateTimeField(verbose_name='유통기한')),
            ],
        ),
    ]