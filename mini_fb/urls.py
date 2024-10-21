from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView, UpdateProfileView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),  
    path('profile/<int:pk>/create_status_message', CreateStatusMessageView.as_view(), name='create_status_message'),
    path('profile/<int:pk>/update', UpdateProfileView.as_view(), name='update_profile'),  # Add this line


]