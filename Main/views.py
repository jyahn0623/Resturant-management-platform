from django.shortcuts import render, HttpResponse, Http404, render_to_response, redirect
from .models import Order, Stock
from django.forms.models import modelform_factory
from django.views.generic.edit import DeleteView, UpdateView

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

# 재고 삭제
class StockDelete(DeleteView):
    model = Stock
    success_url = '/Stock/Inquiry/'
    template_name = 'Main/Stock/Stock_read_items.html'
    print("삭제 완료")

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
        return render_to_response('Main/Order/Order_read_items.html', {
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

# 발주 삭제
class OrderDelete(DeleteView):
    model = Order
    success_url = "/Order/Inquiry/"
    template_name = "Main/Order/Order_read_items.html"
