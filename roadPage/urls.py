# roadPage/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_page, name='upload_page'),  # Main upload page
    path('upload/', views.upload_image, name='upload_image'),  # Upload endpoint
]