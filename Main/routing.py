from django.urls import path
from .consumer import OrderConsumer

websocket_urlpatterns=[
    path('Order/State/', OrderConsumer, name='hello'),
]