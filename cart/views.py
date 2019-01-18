from unittest import result

from django.http import JsonResponse
from django.shortcuts import render


# 购物车
from cart.models import ShoppingCart
from goods.models import Goods


def cart(requset):
    if requset.method == 'GET':
        # 获取数据
        session_goods = requset.session.get('goods')
        result = []
        for se_goods in session_goods:
            goods = Goods.objects.filter(pk=se_goods[0]).first()
            total_price = goods.shop_price * se_goods[1]
            data = [goods, se_goods[1], se_goods[2], total_price]
            result.append(data)
        return render(requset, 'cart.html', {'result': result})


# 添加商品
def add_cart(requset):
    if requset.method == 'POST':
        # 接收商品id值个商品数量
        # 组装储存格式[goods_id, num , is_select]
        # 组装商品格式[[goods_id, num ,is_select],[goods_id,num,is_select]]
        goods_id = int(requset.POST.get('goods_id'))
        goods_num = int(requset.POST.get('goods_num'))
        goods_list = [goods_id, goods_num, 1]

        session_goods = requset.session.get('goods')
        if session_goods:
            # 添加的商品，则新增

            flag = True
            for se_goods in session_goods:
                if se_goods[0] == goods_id:
                    se_goods[1] += goods_num
                    flag = False
            if flag:
                # 添加重复的商品则修改商品数量
                session_goods.append(goods_list)
            requset.session['goods'] = session_goods
            count = len(session_goods)
        else:
            # 第一次添加
            # 格式为[goods_id, num, is_select]
            requset.session['goods'] = [goods_list]
            count = 1
    return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


# 购物车商品数量
def cart_num(requets):
    if requets.method == 'GET':
        session_goods = requets.session.get('goods')
        count = len(session_goods) if session_goods else 0
        return JsonResponse({'code':200, 'msg':'请求成功','count':count})


# 总价
def cart_price(request):
    if request.method == 'GET':
        session_goods = request.session.get('goods')
        all_total = len(session_goods) if session_goods else 0
        all_price = 0
        is_select_num = 0

        for se_goods in session_goods:
            if se_goods[2]:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                all_price += goods.shop_price * se_goods[1]
                is_select_num += 1
        return JsonResponse({'code':200, 'msg':'请求成功', 'all_price':all_price, 'is_select_num':is_select_num, 'all_total':all_total})


# 修改
def change_cart(request):
    if request.method == 'POST':
        #修改session
        goods_id = int(request.POST.get('goods_id'))
        goods_num = request.POST.get('goods_num')
        goods_select = request.POST.get('goods_select')

        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if se_goods[0] == goods_id:
                se_goods[1] = int(goods_num) if goods_num else se_goods[1]
                se_goods[2] = int(goods_select) if goods_select else se_goods[2]
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


# 删除购物车
def del_cart(request, id):
    if request.method == 'POST':
        session_goods = request.session.get('goods')
        for se_goods in session_goods:
            if se_goods[0] == id:
                session_goods.remove(se_goods)
                break
        request.session['goods'] = session_goods
        ShoppingCart.objects.filter(goods_id=id).delete()
        return JsonResponse({'code':200, 'msg':'请求成功'})
