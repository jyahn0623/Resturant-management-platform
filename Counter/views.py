from django.shortcuts import render, HttpResponse
from django.views import View
from Main.models import Table_order, Order_sheet, Profit, Menu
import json
from django.core import serializers
# Create your views here.

class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Counter/main.html', {})

class OrderSheetInfo(View):
    def get(self, request, *args, **kwargs):
        datas = {}
        try:
            os = Order_sheet.objects.get(os_table_no=kwargs.get('id'), os_status=True)
            to = Table_order.objects.filter(to_order_sheet=os, to_isActive=True).exclude(to_status='취소')
        
            datas['table_info'] = os
            datas['menu_info'] = to
            datas['amount'] = getMenuMoneySum(to)
        except Exception as e:
            pass     
        return render(request, 'Counter/table-information.html', {'table' : datas,})

# 결제 완료 시
# amount - 액수
# sheet_no - 테이블 번호
def finishedPayment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        sheet_no = request.POST.get('sheet_no')
        try:
            os= Order_sheet.objects.get(id=sheet_no)
            to = Table_order.objects.filter(to_order_sheet=os, to_isActive=True).exclude(to_status='취소').update(to_isActive=False)
            Profit.objects.create(
                p_detail='음식 판매',
                p_amount=amount,
                p_os=os
            )
            os.inactivateOrdersheet()
            message = '정상 처리 되었습니다.'
        except Exception as e:
            print(e)
            message = '처리 도중 에러가 발생했습니다.'

        return HttpResponse(json.dumps({'message' : message}), content_type="json/application")

# 주문서 총액 구하는 함수
def getMenuMoneySum(menus):
    amount_price = 0
    for menu in menus:
        amount_price += (int(menu.to_menu.m_price) * menu.to_count)
    return amount_price

class OrderSheetUpdate(View):
    def get(self, request, *args, **kwargs):
        datas = {}
        try:
            print(kwargs.get('id'))
            os = Order_sheet.objects.get(pk=kwargs.get('id'))
            to = Table_order.objects.filter(to_order_sheet=os, to_isActive=True)
            datas['os'] = os
            datas['to'] = to
            datas['menus'] = Menu.objects.all()
            datas['menu'] = serializers.serialize('json', Menu.objects.all())
            datas['json_data'] = serializers.serialize('json', to)
        
        except Exception as e:
            print(e)
        return render(request, 'Counter/table-modified.html', datas)

    def post(self, request, *args, **kwargs):
        # 수정 데이터 값
        new_datas = json.loads(request.POST.get('new_datas'))
        try:
            os = Order_sheet.objects.get(pk=kwargs.get('id'))
            # 기존 데이터 삭제 후 새로운 데이터 생성
            to = Table_order.objects.filter(to_order_sheet=os).delete()
            
            for menu in new_datas['menu']:
                tmp = Menu.objects.get(pk=menu)
                Table_order.objects.create(
                    to_menu=tmp,
                    to_count=new_datas['menu'][menu],
                    to_status='완료',
                    to_isActive=True,
                    to_order_sheet=os
                )
        except Exception as e:
            print(e)
        return HttpResponse('hello')
