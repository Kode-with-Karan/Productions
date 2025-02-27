from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transactions, name='transactions'),
    path('earnings/', views.earnings, name='earnings'),
]
