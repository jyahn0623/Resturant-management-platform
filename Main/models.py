from django.db import models

# Create your models here.

class Stock(models.Model):
    class Meta:
        verbose_name = '재고'
        verbose_name_plural = '재고'

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
            Stocklog(sl_log=changed, sl_category='재고').save()
            super(Stock, self).save(*args, **kwargs)
        except Stock.DoesNotExist:
            super(Stock, self).save(*args, **kwargs)
            Stocklog(sl_log="재고 목록 {0} 생성".format(self.s_name), sl_category='재고').save()

    def delete(self, *args, **kwargs):
        Stocklog(sl_log='재고 목록 {0} 삭제'.format(self.s_name), sl_category='재고').save()
        super(Stock, self).delete()

    def stock_checking(self):
        if self.s_count == 0 and self.s_status == True:
            return False
        else:
            return True
    

        
class Order(models.Model):
    class Meta:
        verbose_name = '발주'
        verbose_name_plural = '발주'

    o_name = models.CharField(max_length=30, verbose_name="품명")
    o_count = models.FloatField(verbose_name="수량")
    o_unit = models.CharField(max_length=10, verbose_name='단위', blank=True, null=True)
    o_order_at = models.DateTimeField(verbose_name='주문일자')
    o_target = models.CharField(max_length=30, verbose_name="거래처", null=True)
    o_note = models.CharField(max_length=50, verbose_name="비고", null=True)
    o_status = models.BooleanField(verbose_name='상태', default=False)

    def save(self, *args, **kwargs):
        try:
            obj = Order.objects.get(id=self.id)
            changed = ""
            for field in obj._meta.fields:
                if getattr(obj, field.name, None) != getattr(self, field.name, None):
                    changed += '{0}의 {1}의 값이 {2}->{3}로 변경,  '.format(self.o_name, field.verbose_name,\
                         getattr(obj, field.name, None), getattr(self, field.name, None))
            Stocklog(sl_log=changed).save()
        except Order.DoesNotExist:
            Stocklog(sl_log='발주 목록 {0} 생성'.format(self.o_name), sl_category="발주").save()
        super(Order, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        Stocklog(sl_log='발주 목록 {0} 삭제'.format(self.o_name), sl_category="발주").save()
        super(Order, self).delete(*args, **kwargs)



class Stocklog(models.Model):
    class Meta:
        verbose_name = '재고 기록'
        verbose_name_plural = '재고 기록'
    sl_category = models.CharField(max_length=10, null=True)
    sl_log = models.CharField(max_length=100, verbose_name="변경사항")
    sl_created_at = models.DateTimeField(verbose_name="로그 시간", auto_now=True)



def directory_url(instance, filename):
    print(instance, filename)
    return '{0}/{1}'.format("청주대학교 식당", filename) 

class Menu(models.Model):
    class Meta:
        verbose_name = '메뉴'
        verbose_name_plural = '메뉴'

    m_name = models.CharField(max_length=20, verbose_name="메뉴 이름")
    m_price = models.PositiveIntegerField(verbose_name="가격")
    m_explain = models.CharField(max_length=100, verbose_name="설명")
    m_pic = models.ImageField(verbose_name="사진", null=True, blank=True, upload_to=directory_url)

    def __str__(self):
        return self.m_name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("main:sell_delete", kwargs={"pk": self.pk})

class Order_sheet(models.Model):
    class Meta:
        verbose_name = '주문서'
        verbose_name_plural = '주문서'
    os_table_no = models.PositiveIntegerField(verbose_name="테이블 번호")
    os_amount = models.PositiveIntegerField(verbose_name="총액")
    os_order_date = models.DateTimeField(verbose_name="주문 시간", auto_now=True)
    os_status = models.BooleanField(verbose_name='활성여부', default=True)

    def inactivateOrdersheet(self):
        if self.os_status == False:
            return
        self.os_status = False
        self.save(update_fields=['os_status', ])
        
class Table_order(models.Model):
    class Meta:
        verbose_name = '주문 메뉴'
        verbose_name_plural = '주문 메뉴'
    to_menu = models.ForeignKey("Main.Menu", verbose_name="메뉴", on_delete=models.CASCADE)
    to_count = models.PositiveIntegerField(verbose_name="개수")
    to_status = models.CharField(verbose_name="주문 상태", max_length=10)
    to_isActive = models.BooleanField(default=True)
    to_order_sheet = models.ForeignKey("Main.Order_sheet", verbose_name="주문서", on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        print(getattr(self, 'to_status', None))
        super(Table_order, self).save(*args, **kwargs)
 
class Profit(models.Model):
    class Meta:
        verbose_name = '수익'
        verbose_name_plural = '수익'
    p_profit_date = models.DateTimeField(auto_now_add=True)
    p_detail = models.CharField(max_length=100)
    p_amount = models.IntegerField(default=0)
    p_os = models.ForeignKey('Main.Order_sheet', on_delete=models.CASCADE, null=True)
    
class Spending(models.Model):
    class Meta:
        verbose_name = '지출'
        verbose_name_plural = '지출'
    s_spending_date = models.DateTimeField(auto_now_add=True)
    s_detail = models.CharField(max_length=100, default="")
    s_expense = models.IntegerField(default=0)
    