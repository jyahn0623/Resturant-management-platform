from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', mainView.as_view(), name='main'),
    path('hi/', test2.as_view(), name='test'),
    path('Do/Order/', views.doOrder, name='doOrder')
]
