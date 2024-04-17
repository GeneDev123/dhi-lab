from django.urls import path
from . import views

urlpatterns = [
    path('accounts/<str:login_or_register_param>/', views.user_login_and_register, name='login-register'),
    path('profile/is-updating=<int:is_updating_user_data>', views.user_profile, name='user-profile'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('chatbot-modal/', views.chatbot_modal, name='chatbot-modal'),
    path('filter-symptoms/', views.filter_symptoms, name='filter-symptoms'),
    path('classify-symptoms/', views.classify_symptoms, name='classify-symptoms'),
    path('chatbot/', views.chatbot_page, name='chatbot-page'),
    path('doctors/', views.doctors_page, name='doctors-page'),
    path('', views.home, name='home'), 

    path('train_chatbot/', views.train_chatbot, name='train-chatbot'),
    # path('api/items/', views.CustomUserList.as_view(), name='user-list'),
    # path('api/items/<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'),
]