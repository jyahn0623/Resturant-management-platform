from django.urls import path, re_path
from . import views
from Main.views import StockDelete, OrderDelete, StockUpdate, OrderUpdate

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
    path('Order/<pk>/Incoming/', views.ajaxIncomingOrder, name="incomingOrder")
]

