import json
from flask import request, jsonify
from app.libs.redprint import RedPrint
from app.models.food import Food
from app.models.user import Member
from app.models.cars import MemberCart
from app.service.member_service import MemberService
from app.utils.common import get_img_abs

api = RedPrint('/order', description='付款')


@api.route('/info', methods=['POST'])
def info():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }
    token = request.headers.get('token')
    uid, token = token.split('#')
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    foods_id = request.form.get('ids')
    print('===============================', foods_id)
    try:
        ids = eval(eval(foods_id))
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
        return jsonify(ctx)
    temp = {}
    pay_price = 0
    food_list = []
    print('---------------------------', ids)
    for id in ids:
        #             {
        #                 id: 22,
        #                 name: "小鸡炖蘑菇",
        #                 price: "85.00",
        #                 pic_url: "/images/food.jpg",
        #                 number: 1,
        #             },
        food = Food.query.get(id)
        membercar = MemberCart.query.filter_by(member_id=member.id, food_id=food.id).first()
        temp['id'] = food.id
        temp['name'] = food.name
        temp['price'] = str(food.price)
        temp['pic_url'] = get_img_abs(food.main_image)
        temp['number'] = membercar.quantity
        food_list.append(temp)
        pay_price += membercar.quantity * food.price

    # default_address: {
    #             name: "编程浪子",
    #             mobile: "12345678901",
    #             detail: "上海市浦东新区XX",
    #         },
    default_address = {
        'name': '小徐',
        'mobile': '13096575416',
        'detail': '上海'
    }

    yun_price = 0
    pay_price = pay_price
    total_price = pay_price + yun_price

    ctx['data']['food'] = food_list
    ctx['data']['default_address'] = default_address
    ctx['data']['yun_price'] = str(yun_price)
    ctx['data']['pay_price'] = str(pay_price)
    ctx['data']['total_price'] = str(total_price)
    print(ctx)
    return jsonify(ctx)
