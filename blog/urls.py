from django.urls import path
from django.conf import settings
from . import views
urlpatterns = [
    path(r'', views.ShowAllView.as_view(), name="show_all"),
    #path#(r'create_comment', views.CreateComment.as_view(), name="create_comment")

]