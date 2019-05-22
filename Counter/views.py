from django.shortcuts import render, HttpResponse
from django.views import View
from Main.models import Table_order, Order_sheet, Profit
import json
# Create your views here.

class Main(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'Counter/main.html', {})

class OrderSheetInfo(View):
    def get(self, request, *args, **kwargs):
        datas = {}
        try:
            os = Order_sheet.objects.get(os_table_no=kwargs.get('id'), os_status=True)
            to = Table_order.objects.filter(to_order_sheet=os)
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
