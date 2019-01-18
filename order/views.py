from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from order.models import OrderInfo, OrderGoods
from utils.functions import get_order_sn


def order(request):
    if request.method == 'GET':
        return render(request, 'user_center_order.html')


# 结算商品
def place_order(request):
    if request.method == 'GET':
        # 获取当前登录的用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        # 小计
        total_price = 0
        for cart in carts:
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            total_price += price
        return render(request, 'place_order.html', {'total_price': total_price, 'carts': carts})


def make_order(request):
    if request.method == 'POST':
        # 创建订单
        # 创建订单详情
        # 购物车删除已经下单的商品
        user_id = request.session['user_id']

        shop_carts = ShoppingCart.objects.filter(user_id=user_id,
                                                 is_select=1)
        order_mount = 0
        for carts in shop_carts:
            order_mount += carts.nums * carts.goods.shop_price

        order_sn = get_order_sn()
        order = OrderInfo.objects.create(user_id=user_id,
                                 order_sn=order_sn,
                                 order_mount=order_mount)

        for carts in shop_carts:
            OrderGoods.objects.create(order=order,
                                      goods=carts.goods,
                                      goods_nums=carts.nums)
        shop_carts.delete()
        request.session.pop('goods')

        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_order(request):

    if request.method == 'GET':
        user_id = request.session['user_id']
        page = request.GET.get('page', 1)
















