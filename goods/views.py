from django.shortcuts import render

from goods.models import GoodsCategory, Goods


# 首页
def index(request):
    if request.method == 'GET':
        # 如果访问首页，返回渲染index.html页面
        # 方法一：objects==>[Goods]
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            goods = category.goods_set.all()[:4]
            data = [category, goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(request, 'index.html',{'result':result, 'category_type':category_type})


# 商品详情
def detail(request, id):
    if request.method == 'GET':
        goods = Goods.objects.filter(pk=id).first()
        return render(request, 'detail.html',{'goods': goods})

