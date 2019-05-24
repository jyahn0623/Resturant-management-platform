from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RMS.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
# Celery raises ValueError: not enough values to unpack
# 오류를 해결 할 수 있었다.

from django.conf import settings

# Celery Settings
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

app = Celery('RMS', broker=BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL=BROKER_URL,
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False
)

app.conf.beat_schedule = {
    'deleted_success_order' : {
        'task' : 'Main.tasks.deleted_success_order',
        'schedule': 60.0,
        'args' : ()
    },
}


# celery -A 'ProjectName' worker 하면 이 파일이 먼저 실행이 된다.
# 즉, 세팅 파일을 읽고 실행이 되는 거 같다.

# celery -A RMS -B 즉, celery와 beat(스케쥴러)를 동시에 하게 하는 것은
# windows에서 지원을 안 한다.