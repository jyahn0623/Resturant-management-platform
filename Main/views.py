from django.shortcuts import render, HttpResponse, Http404, render_to_response, redirect
from .models import *
from django.forms.models import modelform_factory
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic import ListView
from django.views import View
import json
from django.core import serializers
from django.db.models import F, Sum, Count

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
def getStockHistory(request, page):
    print('request가 들어오냐?')
    bar_size = 5
    offset = 10
    page = int(page)
    datas = Stocklog.objects.all().order_by('-sl_created_at')
    return render(request, 'Main/Stock/stock_read_history.html', {
        'historys' : datas[(int(page)-1)*offset:int(page)*offset],
        'page' : page,
        'page_start_point' : (page-1)//bar_size*bar_size,
        'MAX_SIZE' : len(datas)//offset,
        'PAGE_SIZE' : bar_size
    })

# -------------- 발주 부분 ------------------#
# 발주 등록
def addOrders(request):
    if request.method == 'POST':
        o_name = request.POST.get('name')
        o_number = request.POST.get('number')
        o_date = request.POST.get('date')
        o_unit = request.POST.get('unit')
        o_target = request.POST.get('target')
        o_note = request.POST.get('note')
        
        Order.objects.create(
            o_name = o_name,
            o_count = int(o_number),
            o_order_at = o_date,
            o_unit = o_unit,
            o_target = o_target,
            o_note = o_note,
        )

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
    order = Table_order.objects.filter(to_isActive=True).order_by('-to_order_sheet__os_order_date')
    return render(request, 'Main/Order_State/index.html', {'orders' : order})

# 지난 주문
class PastOrder(ListView):
    model = Table_order
    template_name = 'Main/Order_State/Order_past.html'
    context_object_name = 'datas'

    def get_queryset(self):
        return Table_order.objects.filter(to_isActive=False).order_by('-to_order_sheet__os_order_date')
        

# 주문 완료 처리
class orderDone(View):
    def post(self, request, *args, **kwargs):
        order_pk = kwargs.get('pk')
        obj = Table_order.objects.get(pk=order_pk)
        obj.to_status = '완료'
        obj.save(update_fields=['to_status', ])
        return HttpResponse(json.dumps({'status' : '완료', }), content_type="json/application")

# 주문 취소 처리
class orderCancel(View):
    def post(self, request, **kwargs):
        order_pk = kwargs.get('pk')
        obj = Table_order.objects.get(pk=order_pk)
        obj.to_status = '취소'
        obj.to_isActive = False
        obj.save(update_fields=['to_status', 'to_isActive'])
        return HttpResponse(json.dumps({'status' : '취소', }), content_type="json/application")



#### 매출 관리 ####

# 수익 관리
class ProfitMain(View):
    def get(self, request, *args, **kwargs):
        profits = Profit.objects.all().order_by('-p_profit_date')
        amount = profits.aggregate(amount=Sum('p_amount'))
        return render(request, 'Main/Profit/main.html', {'profits' : profits, 'amount' : amount['amount']})

class ProfitSearch(View):
    def post(self, request, *args, **kwargs):
        datas = {}
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        if end_date == "" and start_date == "":
            pass
        elif end_date == "":
            datas = Profit.objects.filter(p_profit_date__year=start_date[:4], \
                p_profit_date__month=start_date[5:7], p_profit_date__day=start_date[8:10] ).order_by('-p_profit_date')
        else:
            datas = Profit.objects.filter(p_profit_date__gte=start_date, p_profit_date__lte=end_date).order_by('-p_profit_date')
        amount = datas.aggregate(amount=Sum('p_amount'))
        return render(request, 'Main/Profit/main.html', {'profits' : datas, 'amount' : amount['amount']})

# 지출 관리
class SpendingMain(View):
    def get(self, request, *args, **kwargs):
        datas = Spending.objects.all().order_by('-s_spending_date')
        return render(request, 'Main/Profit/Spending_main.html', {'spending' : datas})

class SpendingSearch(View):
    def post(self, request, *args, **kwargs):
        datas = {}
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        if end_date == "" and start_date == "":
            pass
        elif end_date == "":
            datas = Spending.objects.filter(s_spending_date__year=start_date[:4], \
                s_spending_date__month=start_date[5:7], s_spending_date__day=start_date[8:10] ).order_by('-s_sending_date')
        else:
            datas = Spending.objects.filter(s_spending_date__gte=start_date, s_spending_date__lte=end_date).order_by('-s_sending_date')
        return render(request, 'Main/Profit/Spending_main.html', {'spending' : datas, })

### REST API ####
class MenuApi(View):
    def get(self, request, *args, **kwargs):
        datas = Menu.objects.all()
        print(datas)
        datas_to_JSON = serializers.serialize('json', datas)
        print(datas_to_JSON)
        return HttpResponse(datas_to_JSON, content_type="json/application")