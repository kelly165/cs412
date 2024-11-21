from django.urls import path
from .views import (
    ShowAllProfilesView,
    ShowProfilePageView,
    CreateProfileView,
    CreateStatusMessageView,
    UpdateProfileView,
    DeleteStatusMessageView,
    UpdateStatusMessageView,
    CreateFriendView,
    ShowFriendSuggestionsView,
    ShowNewsFeedView,
    CustomLoginView,
)
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile', ShowProfilePageView.as_view(), name='show_profile'),  # Updated: No pk
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('status/create_status/', CreateStatusMessageView.as_view(), name='create_status_message'),  # Updated: No pk
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),  # Updated: No pk
    path('status/<int:pk>/delete/', DeleteStatusMessageView.as_view(), name='delete_status_message'),
    path('status/<int:pk>/update/', UpdateStatusMessageView.as_view(), name='update_status_message'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),  # Keep pk for other
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),  # Updated: No pk
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),  # Updated: No pk
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'),  # Custom logout template
]
