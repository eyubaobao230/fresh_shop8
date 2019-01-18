from django.urls import path

from order import views

urlpatterns = [
    path('order', views.order, name='order'),
    # 结算商品
    path('place_order', views.place_order, name='place_order'),
    # 创建订单
    path('make_order/', views.make_order, name='make_order'),

]