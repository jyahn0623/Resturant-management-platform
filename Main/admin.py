from django.contrib import admin
from .models import *
# Register your models here.

class UserView(admin.ModelAdmin):
    fieldsets = [
        ('소속정보', {'fields': ['restaurant']}),
        ('개인정보', {'fields' : ['name', 'phone', 'e_mail', 'user_bank', 'user_banknumber']}),
        ('계정정보', {'fields': ['user_id', 'user_pw', 'user_pic']})
    ]

class EmployeeView(admin.ModelAdmin):
    fieldsets = [
        ('소속정보', {'fields': ['restaurant']}),
        ('개인정보', {'fields' : ['employee_name', 'employee_phone', 'employee_email', 'employee_address', 'sex', 'resident_number']}),
        ('관리정보', {'fields': ['employee_bank', 'employee_banknumber', 'employee_pic', 'employee_isdelete']})
    ]

admin.site.register(Order)
admin.site.register(Stock)
admin.site.register(Stocklog)
admin.site.register(Menu)
admin.site.register(Table_order)
admin.site.register(Order_sheet)
admin.site.register(Restaurant)
admin.site.register(User, UserView)
admin.site.register(Employee, EmployeeView)
admin.site.register(Education)
admin.site.register(Iseducation)
admin.site.register(Work)
admin.site.register(Pay)
admin.site.register(Hire)
admin.site.register(Resume)