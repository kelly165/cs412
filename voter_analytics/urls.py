# urls.py
from django.urls import path
from .views import VoterListView, GraphView
from . import views

urlpatterns = [
    path('', VoterListView.as_view(), name='voters'),  
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', GraphView.as_view(), name='graphs'),
]