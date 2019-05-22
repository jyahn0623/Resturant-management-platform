from django.urls import path
from .views import *
from . import views
app_name = 'counter'
urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('OrderSheet/<int:id>/', OrderSheetInfo.as_view(), name='order-info'),
    path('Payment/', views.finishedPayment, name='finishedPayment')
]
