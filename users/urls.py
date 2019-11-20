"""为应用程序users定义URL模式"""
from django.urls import path
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
# from .forms import MyLoginView
from . import views

urlpatterns = [
    # 登陆页面
    path(r'login/', views.LoginView.as_view(), name='login'),
    # path(r'login/', views.custom_login, name='login'),
    # 注销页面
    path(r'logout/', views.logout_view, name='logout'),

    # 用户管理
    path('user_list/', views.UsersView.as_view(), name='user_list'),
    path('user_add/', views.UserAddView.as_view(), name='user_add'),

]
