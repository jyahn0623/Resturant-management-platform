from django.urls import path, re_path
from . import views
from Main.views import *

app_name = 'main'
urlpatterns = [
    path('Stock/', views.stockMain, name="stock"),
    path('Stock/Inquiry/', views.readItems, name="readItems"),
    path('Stock/Add/Items/', views.addItems, name="addItems"),
    path('Stock/<int:pk>/Delete/', StockDelete.as_view(), name='deleteItem'),
    path('Stock/<int:pk>/Edit/', StockUpdate.as_view(), name='updateItem'),
    path('Stock/<pk>/Update/', views.ajaxStockUpdate, name="ajaxStockUpdate"),
    path('Order/Inquiry/', views.readOrders, name='readOrders'),
    path('Order/Add/Items/', views.addOrders, name='addOrders'),
    path('Order/<int:pk>/Delete/', OrderDelete.as_view(), name='deleteOrders'),
    path('Order/<int:pk>/Edit/', OrderUpdate.as_view(), name="updateOrder"),
    path('Order/<pk>/Incoming/', views.ajaxIncomingOrder, name="incomingOrder"),
    path('Stock/History/', views.getStockHistory, name="getStockHistory"),

    path('Sell/', views.sell, name="sell"),
    path('Sell/Admin/', views.sellAdmin, name="sellAdmin"),
    path('Sell/Menu/Register/', views.sell_registerMenu, name="sell_registerMenu"),
    path('Sell/<int:pk>/Delete/', SellDelete.as_view(), name="sell_delete"),
    path('Sell/<int:pk>/Update/', SellUpdate.as_view(), name="sell_update"),

    path('Order/State/', views.orderState, name='orderState'),
    path('ajax/Order/<pk>/Done/', orderDone.as_view(), name='orderDone'),
    path('ajax/Order/<pk>/Cancel/', orderCancel.as_view(), name='orderCancel')
]

