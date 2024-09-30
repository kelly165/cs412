# restaurant/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main, name='restaurant-main'),
    path('order/', views.order, name='restaurant-order'),
    path('confirmation/', views.confirmation, name='restaurant-confirmation'),
]