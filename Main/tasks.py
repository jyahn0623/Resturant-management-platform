from __future__ import absolute_import
from RMS.celery_settings import app

@app.task
def deleted_success_order(*args):
    from .models import Order
    datas = Order.objects.filter(o_status=True).update(o_isAcitve=False)
    print('비활성화 처리 완료')

