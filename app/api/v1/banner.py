import requests
from time import sleep
from flask import request, current_app, jsonify

from app.libs.redprint import RedPrint
from app.models.food import *
from app.utils.common import get_img_abs

api = RedPrint(name='foods', description='商品模型')  # 传入两个参数，一个是路由，一个是对红图的描述


@api.route('/banners', methods=['GET'])
def banners():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    foods = Food.query.filter_by(status=1).limit(3).all()
    banners = [{'id': food.id, 'pic_url': get_img_abs(food.main_image)} for food in foods]

    print(banners)
    ctx['data']['banners'] = banners
    return jsonify(ctx)


@api.route('/categorys', methods=['GET'])
def category():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    categorys = Category.query.all()
    categorys = [{'id': category.id, 'name': category.name} for category in categorys]
    categorys.insert(0, {'id': 0, "name": "全部"})
    ctx['data']['categorys'] = categorys
    return jsonify(ctx)


@api.route('/lists', methods=['GET'])
def list():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {},
        'ismore': 1
    }
    try:
        cid = int(request.args.get('cid'))
        page = int(request.args.get("page"))
        if cid == 0:
            fs = Food.query.filter_by(status=1)
        else:
            fs = Food.query.filter_by(cat_id=cid, status=1)

        if page < 1:
            page = 1
        pagesize = 1  # 每页展示多少个
        offset = (page - 1) * pagesize
        fs = fs.offset(offset).limit(pagesize).all()
        if len(fs) <= 0:
            ctx['ismore'] = 0
        foods = []
        for food in fs:
            temp = {}
            temp['id'] = food.id
            temp['name'] = food.name
            temp['min_price'] = food.min_price
            temp['price'] = str(food.price)
            temp['pic_url'] = get_img_abs(food.main_image)
            foods.append(temp)

        ctx['data']['goods'] = foods
    except Exception as e:
        print(e)
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
    return jsonify(ctx)


@api.route('/info', methods=['GET'])
def info():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }
    try:
        id = request.args.get('id')
        food = Food.query.get(id)
        imgs = food.imgs
        info = {
            "id": food.id,
            "name": food.name,
            "summary": food.summary,
            "total_count": food.total_count,
            "comment_count": food.comment_count,
            "stock": food.stock,
            "price": str(food.price),
            "main_image": food.main_image,
            "pics": [get_img_abs(str(img.img)) for img in imgs]
        }
        ctx['data']['info'] = info
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'

    return jsonify(ctx)
