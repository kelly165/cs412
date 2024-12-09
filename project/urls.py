from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import RegisterView, CustomLoginView, ClothingItemCreateView, CreateOutfitView, OutfitDeleteView, EditClothingItemView, DeleteClothingItemView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', views.ClothingItemListView.as_view(), name='clothing_item_list'),
    path('item/<int:pk>/', views.ClothingItemDetailView.as_view(), name='clothing_item_detail'),
    path('outfits/', views.OutfitListView.as_view(), name='outfit_list'),
    path('outfit/<int:pk>/', views.OutfitDetailView.as_view(), name='outfit_detail'),
    path('clothingitem/<int:pk>/', views.ClothingItemDetailView.as_view(), name='clothingitem_detail'),
    path('login/', CustomLoginView.as_view(template_name = 'registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='project/logged_out.html'), name='logout'),  
    path('register/', RegisterView.as_view(), name='register'),
    path('add/', ClothingItemCreateView.as_view(), name='add_clothing_item'),
    path('create_outfit/', CreateOutfitView.as_view(), name='create_outfit'),
    path('random_outfit/', views.RandomOutfitView.as_view(), name='random_outfit'),
    path('outfit/<int:pk>/delete/', OutfitDeleteView.as_view(), name='outfit_delete'),
    path('clothingitem/edit/<int:pk>/', EditClothingItemView.as_view(), name='edit_clothing_item'),
    path('clothingitem/delete/<int:pk>/', DeleteClothingItemView.as_view(), name='delete_clothing_item'),

]
