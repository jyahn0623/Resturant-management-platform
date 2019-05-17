from django.urls import path
from . import consumer

websocket_urlpatterns =[
    path('Test', consumer.RMSConsumer),
]