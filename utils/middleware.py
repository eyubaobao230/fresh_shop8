import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class AuthMiddleware(MiddlewareMixin):

    # 登录校验
    def process_request(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        #     登录校验，哪些要登录校验,哪些不需要
        path = request.path
        #不需要登录校验
        not_need_check = ['/user/register/', '/media/.*', '/user/login/', '/goods/index/', '/goods/detail/.*/', '/cart/.*/']
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path路径为不需要登录做效验的路由
                return None
        if not user_id:
            # 如果session中没有user_id字段，则跳转到登录
            return HttpResponseRedirect(reverse('user:login'))

        # 通过user_id获取user对象
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return HttpResponseRedirect(reverse('user:login'))
        # 获取到user，则设置全局用户对象
        request.user = user
        return None

# 同步
class SessionTobMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        user_id = request.session.get('user_id')
        if user_id:
            # 同步
            # 判断session中的商品是否存在于数据库中，如果存在，则更新
            # 如果不存在，则创建
            # 同步数据裤到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    # se_goods结构[goods_id, num, is_select]
                    cart = ShoppingCart.objects.filter(user_id=user_id,
                                                       goods_id=se_goods[0]).first()
                    if cart:
                        # 更新商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])
            # 同步数据库中的数据库session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id).all()
            # 组装多个商品格式
            if db_carts:
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods

        return response











