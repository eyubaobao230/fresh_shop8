from django.urls import path

from user import views

urlpatterns = [
    # 登录
    path('login/', views.login, name='login'),
    # 注册
    path('register/', views.register, name='register'),
    path('user_center_info/', views.user_center_info, name='user_center_info'),
    # 退出
    path('logout/', views.logout, name='logout'),
    # 收货地址
    path('user_site/', views.user_site, name='user_site'),

]