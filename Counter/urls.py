from django.urls import path
from .views import *
from . import views
app_name = 'counter'
urlpatterns = [
    path('', Main.as_view(), name='main'),
    path('OrderSheet/<int:id>/', OrderSheetInfo.as_view(), name='order-info'),
    path('OrderSheet/<int:id>/update', OrderSheetUpdate.as_view(), name='order-update'),
    path('Payment/', views.finishedPayment, name='finishedPayment')
]
