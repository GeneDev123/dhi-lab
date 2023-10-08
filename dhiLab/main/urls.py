from django.urls import path
from . import views

urlpatterns = [
    path('accounts/<str:login_or_register_param>/', views.user_login_and_register, name='login-register'),
    path('profile/', views.user_profile, name='user-profile'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'), 

    # path('api/items/', views.CustomUserList.as_view(), name='user-list'),
    # path('api/items/<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'),
]