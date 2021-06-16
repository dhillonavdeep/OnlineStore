from django.urls import path
from . import views

urlpatterns = [
    path('',views.home),
    path('contact',views.contact),
    path('products',views.products),
    path('customer/<str:pk_test>/',views.customer),
]
