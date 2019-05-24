from __future__ import absolute_import
from RMS.celery_settings import app

@app.task
def deleted_success_order(*args):
    from .models import Table_order
    datas = Table_order.objects.filter(to_status="완료").update(to_isActive=False)
    print('비활성화 처리 완료')

