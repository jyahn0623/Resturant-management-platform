from django.db import models

# Create your models here.

class Stock(models.Model):
    s_name = models.CharField(max_length=30)
    s_count = models.IntegerField(verbose_name='재고량', default=0)
    s_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    s_incoming_at = models.DateField(verbose_name='반입일자')
    s_status = models.BooleanField(verbose_name='상태', default=True)
    s_caution_num = models.PositiveIntegerField()
    s_expire_at = models.DateTimeField(verbose_name='유통기한')

class Order(models.Model):
    o_name = models.CharField(max_length=30)
    o_count = models.PositiveIntegerField()
    o_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    o_order_at = models.DateTimeField(verbose_name='주문일자')
    o_status = models.BooleanField(verbose_name='상태', default=False)
    