from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='library/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.user_landing, name='user_landing'),
    path('cancel/<int:request_id>/', views.cancel_request, name='cancel_request'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_landing/', views.user_landing, name='user_landing'),
    path('request_book/', views.request_book, name='request_book'),
]