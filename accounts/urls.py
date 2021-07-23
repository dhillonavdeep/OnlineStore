from django.urls import path
#importing this for authenticating views
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),

    #user can change profile info here
    path('account/', views.accountSettings, name="account"),

    path('user/',views.userPage,name="home"),
    path('contact',views.contact,),
    path('products',views.products,name="products"),
    path('customer/<str:pk_test>/',views.customer,name="customer"),

    path('create_order/<str:pk>',views.createOrder,name="create_order"),
    path('update_order/<str:pk>/',views.updateOrder,name="update_order"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete_order"),

    path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password_"),
    path('password_reset_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

]
