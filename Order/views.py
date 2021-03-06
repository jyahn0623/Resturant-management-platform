from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from Main.models import Menu as m_Menu
from Main.models import Table_order as to, Order_sheet as os
import json
# Create your views here.
class mainView(View):
    def get(self, request):
        request.session['name'] = 'ajy'
        return render(request, "Order/main.html")

    def post(self, request):
        user_id = request.POST.get('id')
        user_pw = request.POST.get('pw')
        print(user_id, user_pw)

        menu = m_Menu.objects.all()
        return render(request, 'Order/order.html', {'menus' : menu})

def doOrder(request):
    datas_to_json = json.loads(request.POST.get('datas', ''))
    # 프로토 타입에서는 table num를 1로 가정
    
    # 이미 주문된 상태라면 기존 시트에 추가가 되게 함
    try:
        order_sheet=os.objects.get(os_status=True, os_table_no=1)
    except os.DoesNotExist:
        order_sheet=os.objects.create(
            os_table_no=1,
            os_amount=0,
        )
    for menu in datas_to_json['menu']:
        if datas_to_json['menu'][menu] <= 0:
            continue   
        orderd_menu = to.objects.create(
            to_menu=m_Menu.objects.get(pk=menu),
            to_count=datas_to_json['menu'][menu],
            to_status='주문',
            to_order_sheet=order_sheet
        )
         
    return HttpResponse(json.dumps({'message' : '주문이 완료되었습니다.'}), content_type="application/json")


class test2(View):
    def get(self, request, *args, **kwargs):          
        a = request.session.keys()
        return render(request, 'Order/test1.html', {'datas' : a})

    def post(self, request, *args, **kwargs):
        print(request.keys())
        return redirect(reverse('test'))