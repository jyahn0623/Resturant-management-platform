from django.urls import path, re_path
from . import views
from Main.views import *

app_name = 'main'
urlpatterns = [
    path('Stock/', views.stockMain, name="stock"),
    path('Stock/Inquiry/', views.readItems, name="readItems"),
    path('Stock/Add/Items/', views.addItems, name="addItems"),
    path('Stock/<int:pk>/Delete/', StockDelete.as_view(), name='deleteItem'),
    path('Stock/<int:pk>/Edit/', StockUpdate.as_view(), name='updateItem'),
    path('Stock/<pk>/Update/', views.ajaxStockUpdate, name="ajaxStockUpdate"),
    path('Order/Inquiry/', views.readOrders, name='readOrders'),
    path('Order/Add/Items/', views.addOrders, name='addOrders'),
    path('Order/<int:pk>/Delete/', OrderDelete.as_view(), name='deleteOrders'),
    path('Order/<int:pk>/Edit/', OrderUpdate.as_view(), name="updateOrder"),
    path('Order/<pk>/Incoming/', views.ajaxIncomingOrder, name="incomingOrder"),
    path('Stock/History/', views.getStockHistory, name="getStockHistory"),

    path('Sell/', views.sell, name="sell"),
    path('Sell/Admin/', views.sellAdmin, name="sellAdmin"),
    path('Sell/Menu/Register/', views.sell_registerMenu, name="sell_registerMenu"),
    path('Sell/<int:pk>/Delete/', SellDelete.as_view(), name="sell_delete"),
    path('Sell/<int:pk>/Update/', SellUpdate.as_view(), name="sell_update"),

    path('Order/State/', views.orderState, name='orderState'),
    path('ajax/Order/<pk>/Done/', orderDone.as_view(), name='orderDone'),
    path('ajax/Order/<pk>/Cancel/', orderCancel.as_view(), name='orderCancel'),

    #인사관리
    path('Human', views.Human, name='Human'), #인사관리 메인페이지
    path('Human/Employee/Enrollment', views.EmpEnrollment, name='EmpEnrollment'), #사원등록
    path('Human/Employee/Inquire', views.EmpInquire, name='EmpInquire'), #사원조회
    path('Human/Employee/Delete/<int:pk>', views.EmpDelete, name='EmpDelete'), #사원삭제
    path('Human/Employee/Save/<int:pk>', views.EmpSave, name='EmpSave'), #사원변경
    path('Human/Education/Enrollment', views.EduEnrollment, name='EduEnrollment'), #교육등록
    path('Human/Education/Inquire', views.EduInquire, name='EduInquire'), #교육조회
    path('Human/Education/Save/<int:pk>', views.EduSave, name='EduSave'), #교육변경
    path('Human/Education/Delete/<int:pk>', views.EduDelete, name='EduDelete'), #교육삭제
    path('Human/Work/Enrollment', views.WorkEnrollment, name='WorkEnrollment'), #근무등록
    path('Human/Work/Inquire', views.WorkInquire, name='WorkInquire'), #근무조회
    path('Human/Work/Save/<int:pk>', views.WorkSave, name='WorkSave'), #근무변경
    path('Human/Work/Delete/<int:pk>', views.WorkDelete, name='WorkDelete'), #근무삭제
    path('Human/Payroll_Calculator', views.PayCal, name='PayCal'), #급여계산기
    path('Human/Pay/Enrollment', views.PayEnrollment, name='PayEnrollment'), #급여등록
    path('Human/Pay/Inquire', views.PayInquire, name='PayInquire'), #급여조회
    path('Human/Pay/Save/<int:pk>', views.PaySave, name='PaySave'), #급여변경
    path('Human/Pay/Delete/<int:pk>', views.PayDelete, name='PayDelete'), #급여삭제
    path('Human/Hire/Enrollment', views.HireEnrollment, name='HireEnrollment'), #채용등록
    path('Human/Hire/Inquire', views.HireInquire, name='HireInquire'), #채용조회
    path('Human/Hire/Detail/<int:pk>', views.HireDetail, name='HireDetail'), #채용세부조회
    path('Hire/Main', views.HireMian, name='HireMain'), #채용메인페이지
    path('Hire/Main/Sign/<int:pk>', views.HireSign, name='HireSign'), #이력서 등록

    # 매출 관리
    path('Profit/', ProfitMain.as_view(), name="profit-main")
]

