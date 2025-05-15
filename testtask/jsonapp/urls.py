from django.urls import path, re_path, register_converter
from . import views

urlpatterns = [
    path('', views.upload_json, name='upload_json'),  # http://127.0.0.1:8000
    path('data/', views.data_list, name='data_list'),  # http://127.0.0.1:8000/data

]