# quotes/urls.py

from django.urls import path
from . import views

urlpatterns = [
    #Setting up URLSfor my pages
    path('base/', views.quote, name='main_page'),      
    path('quote/', views.quote, name='quote_page'), 
    path('show_all/', views.show_all, name='show_all_page'), 
    path('about/', views.about, name='about_page'),  
]
