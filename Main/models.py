from django.db import models

# Create your models here.

class Stock(models.Model):
    s_name = models.CharField(max_length=30, verbose_name="재고명")
    s_count = models.IntegerField(verbose_name='재고량', default=0)
    s_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    s_incoming_at = models.DateField(verbose_name='반입일자', null=True, blank=True)
    s_status = models.BooleanField(verbose_name='상태', default=True)
    s_caution_num = models.PositiveIntegerField(verbose_name="경고 수량", null=True, blank=True)
    s_expire_at = models.DateTimeField(verbose_name='유통기한', null=True, blank=True)

    def save(self, *args, **kwargs):
        try:
            stock = Stock.objects.get(pk=getattr(self, 'id', None))
            changed = ""
            for field in stock._meta.fields:
                if getattr(stock, field.name, None) != getattr(self, field.name, None):
                    changed += '{0}의 값이 {1}->{2}로 변경'.format(field.name, getattr(stock, field.name, None), getattr(self, field.name, None))
            Stocklog(sl_name=self, sl_log=changed).save()
            super(Stock, self).save(*args, **kwargs)
        except Stock.DoesNotExist:
            super(Stock, self).save(*args, **kwargs)
            Stocklog(sl_name=self, sl_log="New Instance").save()
        
class Order(models.Model):
    o_name = models.CharField(max_length=30, verbose_name="품명")
    o_count = models.PositiveIntegerField(verbose_name="수량")
    o_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    o_order_at = models.DateTimeField(verbose_name='주문일자')
    o_status = models.BooleanField(verbose_name='상태', default=False)

class Stocklog(models.Model):
    sl_name = models.ForeignKey(Stock, on_delete=models.CASCADE, verbose_name="재고명")
    sl_log = models.CharField(max_length=100, verbose_name="변경사항")