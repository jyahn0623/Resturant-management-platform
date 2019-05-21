from django.shortcuts import render, HttpResponse, Http404, render_to_response, redirect
from .models import *
from django.forms.models import modelform_factory
from django.views.generic.edit import DeleteView, UpdateView
from django.views import View
import json

# -------------- 재고 부분 ------------------#
# Main
def stockMain(request):
    return render(request, 'Main/Stock/main.html')

# 재고 조회
def readItems(request):
    try:
        Stocks = Stock.objects.all()
    except Exception as e:
        Stocks = None

    return render(request, 'Main/Stock/Stock_read_items.html', {
        'Stocks' : Stocks
    })

# 재고 등록
def addItems(request):
    if request.method == 'POST':
        s_name = request.POST.get('name')
        s_count = request.POST.get('number')
        s_unit = request.POST.get('unit')
        s_incoming_at = request.POST.get('date')
        s_caution_num = request.POST.get('alter_number')
        s_expire_at = request.POST.get('expire_date')

        Stock.objects.create(
            s_name = s_name,
            s_count = int(s_count),
            s_unit = s_unit,
            s_incoming_at = s_incoming_at,
            s_caution_num = s_caution_num,
            s_expire_at = s_expire_at
        )
        print("재고 생성 완료")
        return redirect('/Stock/Inquiry/', {
            'Stocks' : Stock.objects.all(),
        })

    return render(request, 'Main/Stock/Stock_add_item.html')

# 재고 수정
class StockUpdate(UpdateView):
    model = Stock
    fields = ['s_name', 's_count', 's_unit', 's_incoming_at', 's_caution_num',
                's_expire_at']
    success_url = '/Stock/Inquiry/'
    template_name = 'Main/Stock/Stock_update_item.html'
    
    def get_initial(self):
        initial = super(StockUpdate, self).get_initial()
        return initial

# 재고 소비 및 충당
def ajaxStockUpdate(request, pk):
    message = ""
    m_count = request.POST.get("change_value")
    type_ = request.POST.get("type")
    data = dict()
    try:
        stock = Stock.objects.get(id=pk)
        if type_ == '0':
            stock.s_count =stock.s_count+float(m_count)
        else:
            stock.s_count =stock.s_count-float(m_count)

        if not stock.stock_checking():
            stock.s_status = False
        else:
            stock.s_status = True

        stock.save(update_fields=['s_count', 's_status'])
        message = "성공적으로 변경되었습니다."
        data['count'] = str(stock.s_count) + stock.s_unit
    except Exception as e:
        message = "처리 도중 오류가 생겼습니다."

    data['message'] = message
    return HttpResponse(json.dumps(data), content_type='application/json')

# 재고 삭제
class StockDelete(DeleteView):
    model = Stock
    success_url = '/Stock/Inquiry/'
    template_name = 'Main/Stock/Stock_read_items.html'

# 이력 조회
def getStockHistory(request):
    return render(request, 'Main/Stock/stock_read_history.html', {
        'historys' : Stocklog.objects.all(),
    })

# -------------- 발주 부분 ------------------#
# 발주 등록
def addOrders(request):
    if request.method == 'POST':
        o_name = request.POST.get('name')
        o_number = request.POST.get('number')
        o_date = request.POST.get('date')
        o_unit = request.POST.get('unit')
        Order.objects.create(
            o_name = o_name,
            o_count = int(o_number),
            o_order_at = o_date,
            o_unit = o_unit
        )
        print("발주 생성 완료")
        return redirect('/Order/Inquiry/', {
            'Orders' : Order.objects.all()
        })
    return render(request, 'Main/Order/Order_add_item.html')

# 발주 조회
def readOrders(request):
    try:
        Orders = Order.objects.all()
    except Exception as e:
        Orders = None

    return render(request, 'Main/Order/Order_read_items.html',{
        'Orders' : Orders,
    })

class OrderUpdate(UpdateView):
    model = Order
    success_url = "/Order/Inquiry/"
    template_name = "Main/Order/Order_update_item.html"
    fields = '__all__'

    def get_initial(self):
        return super().get_initial()

# 발주 반입처리
def ajaxIncomingOrder(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(pk=pk)
        order.o_status = True
        order.save()

        # 반입 처리가 된다면 재고에 추가
        Stock.objects.create(
            s_name=order.o_name,
            s_count=order.o_count,
            s_unit=order.o_unit,
        )
        
        datas = {
            'message' : '성공적으로 처리 되었습니다.',
        }
        return HttpResponse(json.dumps(datas), content_type="application/json")

    return HttpResponse("실패")

# 발주 삭제
class OrderDelete(DeleteView):
    model = Order
    success_url = "/Order/Inquiry/"
    template_name = "Main/Order/Order_read_items.html"

##### 판매 관리 #####
def sell(request):
    return render(request, 'Main/Sell/main.html', {})

def sellAdmin(request):
    return render(request, 'Main/Sell/sell_menu_admin.html', {'menus' : Menu.objects.all() })

def sell_registerMenu(request):
    if request.method == 'POST':
        print(request.POST.keys(), request.POST.values())
        m_name = request.POST.get('name')
        m_price = request.POST.get('price')
        m_explain = request.POST.get('explain')
        m_pic = request.FILES.get('image')

        Menu.objects.create(m_name=m_name, m_price=m_price, m_explain=m_explain, m_pic=m_pic)
        return redirect('/Sell/Admin/')
    return render(request, 'Main/Sell/sell_menu_register.html')

class SellDelete(DeleteView):
    model = Menu
    success_url = "/Sell/Admin/"

class SellUpdate(UpdateView):
    model = Menu
    success_url = "/Sell/Admin/"
    template_name = "Main/Sell/sell_menu_update.html"
    fields = "__all__"

    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        return initial


##### 주문 현황 ### 향후 이식
def orderState(request):
    order = Order_sheet.objects.all()
    return render(request, 'Main/Order_State/index.html', {'orders' : order})

# 주문 완료 처리
def orderDone(request, pk):
    print(pk)
    return HttpResponse('hello')

class orderDone(View):
    def post(self, request, *args, **kwargs):
        order_pk = kwargs.get('pk')
        obj = Table_order.objects.get(pk=order_pk)
        obj.to_status = '완료'
        obj.save(update_fields=['to_status', ])
        return HttpResponse(json.dumps({'status' : '완료', }), content_type="json/application")

class orderCancel(View):
    def post(self, request, **kwargs):
        order_pk = kwargs.get('pk')
        obj = Table_order.objects.get(pk=order_pk)
        obj.to_status = '취소'
        obj.save(update_fields=['to_status', ])
        return HttpResponse(json.dumps({'status' : '취소', }), content_type="json/application")