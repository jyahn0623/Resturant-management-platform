from django.db import models

# Create your models here.

class Stock(models.Model):
    s_name = models.CharField(max_length=30, verbose_name="재고명")
    s_count = models.FloatField(verbose_name='재고량', default=0)
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
                    changed += '{0}의 {1}의 값이 {2}->{3}로 변경,  '.format(self.s_name, field.verbose_name, getattr(stock, field.name, None), getattr(self, field.name, None))
            Stocklog(sl_log=changed).save()
            super(Stock, self).save(*args, **kwargs)
        except Stock.DoesNotExist:
            super(Stock, self).save(*args, **kwargs)
            Stocklog(sl_log="New Instance").save()

    def stock_checking(self):
        if self.s_count == 0 and self.s_status == True:
            return False
        else:
            return True
    

        
class Order(models.Model):
    o_name = models.CharField(max_length=30, verbose_name="품명")
    o_count = models.FloatField(verbose_name="수량")
    o_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    o_order_at = models.DateTimeField(verbose_name='주문일자')
    o_status = models.BooleanField(verbose_name='상태', default=False)

class Stocklog(models.Model):
    sl_log = models.CharField(max_length=100, verbose_name="변경사항")
    sl_created_at = models.DateTimeField(verbose_name="로그 시간", auto_now=True)



def directory_url(instance, filename):
    print(instance, filename)
    return '{0}/{1}'.format("청주대학교 식당", filename) 

class Menu(models.Model):
    m_name = models.CharField(max_length=20, verbose_name="메뉴 이름")
    m_price = models.PositiveIntegerField(verbose_name="가격")
    m_explain = models.CharField(max_length=100, verbose_name="설명")
    m_pic = models.ImageField(verbose_name="사진", null=True, blank=True, upload_to=directory_url)

    def __str__(self):
        return self.m_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("main:sell_delete", kwargs={"pk": self.pk})
    

 
    
    