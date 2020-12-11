from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('view_video/<str:pk>', views.view_video, name='view_video'),
] 