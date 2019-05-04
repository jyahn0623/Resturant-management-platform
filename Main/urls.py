from django.urls import path, re_path
from . import views

app_name = 'main'
urlpatterns = [
    re_path(r'^Stock/', views.Hello, name="stock"),
]

