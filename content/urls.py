from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_content, name='upload_content'),
    path('collaborate/', views.collaborate, name='collaborate'),
    path('category/<str:content_type>/', views.category, name='category'),
    path('content/<int:pk>/', views.content_detail, name='content_detail'),
    path('content_display/<int:pk>/', views.content_display, name='content_display'),
    path('browse/', views.browse_content, name='browse_content'),
    path('edit/<int:pk>/', views.edit_content, name='edit_content'),
    path('delete/<int:pk>/', views.delete_content, name='delete_content'), 
]
