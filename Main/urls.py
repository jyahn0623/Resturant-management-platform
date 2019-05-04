from django.urls import path, re_path
from . import views

app_name = 'main'
urlpatterns = [
    path('Stock/', views.stockMain, name="stock"),
    path('Stock/Inquiry/', views.readItems, name="readItems"),
    path('Stock/Add/Items/', views.addItems, name="addItems"),
    path('Order/Inquiry/', views.readOrders, name='readOrders'),
    path('Order/Add/Items/', views.addOrders, name='addOrders')
]

