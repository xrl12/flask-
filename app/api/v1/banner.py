import requests

from flask import request, current_app, jsonify

from app.libs.redprint import RedPrint

api = RedPrint(name='foods', description='商品模型')  # 传入两个参数，一个是路由，一个是对红图的描述


@api.route('/banners', methods=['GET'])
def banners():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    banners = [
        {
            'id': 1,
            'pic_url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589999926675&di=1f3cc52857073639ff25cb92b4a2767e&imgtype=0&src=http%3A%2F%2Fpic1.16pic.com%2F00%2F53%2F45%2F16pic_5345901_b.jpg'
        }, {
            'id': 2,
            'pic_url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589999926675&di=1f3cc52857073639ff25cb92b4a2767e&imgtype=0&src=http%3A%2F%2Fpic1.16pic.com%2F00%2F53%2F45%2F16pic_5345901_b.jpg'
        }, {
            'id': 3,
            'pic_url': 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589999926675&di=1f3cc52857073639ff25cb92b4a2767e&imgtype=0&src=http%3A%2F%2Fpic1.16pic.com%2F00%2F53%2F45%2F16pic_5345901_b.jpg'
        }
    ]
    ctx['data']['banners'] = banners
    return jsonify(ctx)


@api.route('/categorys', methods=['GET'])
def category():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    categorys = [
        {'id': 0, 'name': "全部"},
        {'id': 1, 'name': "川菜"},
        {'id': 2, 'name': "湘菜"},
        {'id': 3, 'name': "卤菜"}
    ]
    ctx['data']['categorys'] = categorys
    return jsonify(ctx)


@api.route('/lists', methods=['GET'])
def list():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    goods = [
        {
            "id": 1,
            "name": "小鸡炖蘑菇-1",
            "min_price": "1500.00",
            "price": "1500.00",
            "pic_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1204370716,2143384209&fm=26&gp=0.jpg"
        },
        {
            "id": 2,
            "name": "小鸡炖蘑菇-1",
            "min_price": "1500.00",
            "price": "1500.00",
            "pic_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1204370716,2143384209&fm=26&gp=0.jpg"
        },
        {
            "id": 3,
            "name": "小鸡炖蘑菇-1",
            "min_price": "1500.00",
            "price": "1500.00",
            "pic_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1204370716,2143384209&fm=26&gp=0.jpg"
        },
        {
            "id": 4,
            "name": "小鸡炖蘑菇-1",
            "min_price": "1500.00",
            "price": "1500.00",
            "pic_url": "https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1204370716,2143384209&fm=26&gp=0.jpg"
        }

    ]
    ctx['data']['goods'] = goods
    return jsonify(ctx)
