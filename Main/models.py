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
    o_expense = models.IntegerField(verbose_name='비용', default=0)
    o_target = models.CharField(max_length=30, verbose_name="거래처", null=True)
    o_note = models.CharField(max_length=50, verbose_name="비고", null=True)
    o_status = models.BooleanField(verbose_name='상태', default=False)
    o_isAcitve = models.BooleanField(verbose_name="활성화", default=True)

    def save(self, *args, **kwargs):
        try:
            obj = Order.objects.get(id=self.id)
            changed = ""
            for field in obj._meta.fields:
                if getattr(obj, field.name, None) != getattr(self, field.name, None):
                    if field.name == 'o_expense':
                        from .models import Spending
                        s_obj = Spending.objects.get(s_primary_key='{0}{1}'.format('Order', self.pk))
                        s_obj.s_expense = self.o_expense
                        s_obj.save(update_fields=['s_expense',])
                    changed += '{0}의 {1}의 값이 {2}->{3}로 변경,  '.format(self.o_name, field.verbose_name,\
                         getattr(obj, field.name, None), getattr(self, field.name, None))
            Stocklog(sl_log=changed).save()   
            super(Order, self).save(*args, **kwargs)
        except Order.DoesNotExist:
            Stocklog(sl_log='발주 목록 {0} 생성'.format(self.o_name), sl_category="발주").save() 
            super(Order, self).save(*args, **kwargs)
            if self.o_expense != 0:
    
                from .models import Spending
                Spending.objects.create(
                    s_primary_key = '{0}{1}'.format('Order', self.id),
                    s_detail = '{0} 발주 {1}개'.format(self.o_name, self.o_count),
                    s_expense = self.o_expense      
                )
    
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
    p_profit_date = models.DateTimeField(auto_now_add=True, verbose_name='수익 발생일')
    p_detail = models.CharField(max_length=100, verbose_name='내용')
    p_amount = models.IntegerField(default=0, verbose_name='총액')
    p_os = models.ForeignKey('Main.Order_sheet', on_delete=models.CASCADE, null=True)
    
class Spending(models.Model):
    class Meta:
        verbose_name = '지출'
        verbose_name_plural = '지출'
    # 상대 모델명 +인스턴스의 pk 값 
    # 예로, 발주 등록으로 인해 지출 발생 시 Order01
    s_primary_key = models.CharField(max_length=30, unique=True, null=True)
    s_spending_date = models.DateTimeField(auto_now_add=True)
    s_detail = models.CharField(max_length=100, default="", verbose_name='내용')
    s_expense = models.IntegerField(default=0, verbose_name='지출액')


#식당
class Restaurant(models.Model):
    restaurant_name= models.CharField(max_length=50, null=True, blank=True, verbose_name='사명') #식당명
    license_number= models.CharField(max_length=30, null=True, blank=True, verbose_name='사업자번호') #사업자번호
    business= models.CharField(max_length=50, null=True, blank=True, verbose_name='업종') #업종
    restaurant_pic= models.ImageField('식당사진', null=True, blank=True, default="") #식당사진
    registration_date= models.DateField(null=True, blank=True, verbose_name='등록일') # 등록일
    restaurant_address= models.CharField(max_length=100, null=True, blank=True, verbose_name='주소') #주소

    def __str__(self):
        return self.restaurant_name

#사용자
class User(models.Model):
    restaurant= models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명') #식당외래키
    name= models.CharField(max_length=10, null=True, blank=True, verbose_name='이름') #사용자명
    user_id= models.CharField(max_length=30, default="", verbose_name='ID') #사용자id
    user_pw= models.CharField(max_length=30, default="", verbose_name='PW') #사용자pw
    phone= models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='핸드폰') #사용자 핸드폰
    e_mail= models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='이메일') #사용자 이메일
    user_pic= models.ImageField('사진', null=True, blank=True, default="") #사용자 사진
    user_bank= models.CharField(max_length=20, null=True, blank=True, verbose_name='은행명') #사용자은행
    user_banknumber= models.CharField(max_length=30, null=True, blank=True, verbose_name='계좌번호')

    def __str__(self):
        return self.name
    
#종업원
class Employee(models.Model):
    restaurant= models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    employee_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='직원명')
    employee_pic= models.ImageField('종업원사진', null=True, blank=True, default="")
    sex = models.CharField(max_length=10, null=True, blank=True, verbose_name='성별')
    employee_phone= models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='핸드폰') 
    employee_email= models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='이메일')
    resident_number = models.CharField(max_length=20, null=True, blank=True, verbose_name='주민등록번호')
    employee_address= models.CharField(max_length=100, null=True, blank=True, verbose_name='주소')
    employee_bank= models.CharField(max_length=20, null=True, blank=True, verbose_name='은행명')
    employee_banknumber= models.CharField(max_length=30, null=True, blank=True, verbose_name='계좌번호')
    employee_isdelete = models.BooleanField(default=False, verbose_name='삭제')

    def __str__(self):
        return self.employee_name

#교육
class Education(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    education_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='교육명')
    education_content = models.CharField(max_length=100, null=True, blank=True, verbose_name='교육내용 또는 소개')
    education_pic = models.ImageField('교육사진', null=True, blank=True, default="")
    education_isdelete = models.BooleanField(default=False, verbose_name='삭제')


    def __str__(self):
        return self.education_name

#교육이수여부
class Iseducation(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, verbose_name='사원명')
    education = models.ForeignKey(Education, on_delete=models.CASCADE, blank=True, null=True, verbose_name='교육명')
    iscomplete = models.BooleanField(default=False, verbose_name='이수')

    def __str__(self):
        return self.iscomplete

#근무
class Work(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, verbose_name='사원명')
    daytime_work = models.IntegerField(null=True, blank=True, verbose_name='근무시간')
    day_work = models.DateField(blank=True, null=True, verbose_name='근무일')
    work_time = models.CharField(max_length=50, null=True, blank=True, verbose_name='근무파트')
    work_isdelete = models.BooleanField(default=False, verbose_name='삭제')

    def __int__(self):
        return self.daytime_work


#급여
class Pay(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True, verbose_name='사원명')
    work_pay = models.IntegerField(null=True, blank=True, verbose_name='정기수당')
    other_pay = models.IntegerField(null=True, blank=True, verbose_name='특별수당')
    whole_pay = models.IntegerField(null=True, blank=True, verbose_name='총수당')
    day_pay = models.DateTimeField(auto_now_add=True, verbose_name='지급일')
    pay_isdelete = models.BooleanField(default=False, verbose_name='삭제')

    def __int__(self):
        return self.work_pay

#채용등록
class Hire(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='등록자명')
    hire_title = models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='제목')
    hire_content = models.TextField(max_length=400, null=True,blank=True, default="없음", verbose_name='내용')

    def __str__(self):
        return self.hire_title

#채용신청
class Resume(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True, verbose_name='소속명')
    apply_name = models.CharField(max_length=10, null=True, blank=True, verbose_name='이름')
    apply_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='핸드폰')
    apply_email = models.CharField(max_length=50, null=True,blank=True, default="없음", verbose_name='이메일')
    apply_address = models.CharField(max_length=100, null=True, blank=True, verbose_name='주소')
    apply_academic = models.CharField(max_length=20, null=True, blank=True, verbose_name='최종학력')
    apply_career =  models.TextField(max_length=300, null=True, blank=True, verbose_name='경력')
    apply_motive = models.TextField(max_length=300, null=True, blank=True, verbose_name='지원동기')

    def __str__(self):
        return self.apply_name
