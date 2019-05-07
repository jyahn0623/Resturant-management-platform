# Generated by Django 2.1.2 on 2019-05-07 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0010_remove_stocklog_sl_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_name', models.CharField(max_length=20, verbose_name='메뉴 이름')),
                ('m_price', models.PositiveIntegerField(verbose_name='가격')),
                ('m_explain', models.CharField(max_length=100, verbose_name='설명')),
                ('m_pic', models.ImageField(blank=True, null=True, upload_to='', verbose_name='사진')),
            ],
        ),
    ]