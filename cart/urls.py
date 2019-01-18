
from django.urls import path

from cart import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    # 加入购物车
    path('add_cart/', views.add_cart, name='add_cart'),
    # 购物车数量的刷新
    path('cart_num/', views.cart_num, name='cart_num'),
    # 总价
    path('cart_price/', views.cart_price, name='cart_price'),
    # 修改购物车的数量/选择状态
    path('change_cart/', views.change_cart, name='change_cart'),
    # 删除购物车
    path('del_cart/<int:id>/', views.del_cart, name='del_cart'),

]