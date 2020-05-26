from json import loads
from flask import request, jsonify
from app.libs.redprint import RedPrint
from app.models.cars import MemberCart
from app.models.user import Member
from app.models.food import Food
from app.utils.common import get_img_abs
from app import db
from app.service.member_service import MemberService

api = RedPrint('/cars', description='添加购物车')


@api.route('/addcars', methods=['POST'])
def cars():
    ctx = {
        'code': '1',
        'msg': 'OK',
        'data': {}
    }
    try:
        token = request.headers.get('token')
        print(request.headers)
        nums = request.form.get('nums')
        shop_id = request.form.get('id')
        print(token)
        member_id, member_token = token.split('#')  # 获取member id
        member = Member.query.get(member_id)
        token1 = MemberService.geneAuthCode(member)
        if member_token != token1:
            ctx['code'] = -1
            ctx['msg'] = 'token不合法'
            return jsonify(ctx)
        membercart = MemberCart.query.filter(MemberCart.member_id == member_id, MemberCart.food_id == shop_id).first()
        food = Food.query.filter_by(status=1, id=shop_id).first()
        if not member:
            ctx['code'] = -1
            ctx['msg'] = '找不到用户'
        elif int(nums) < 1:
            ctx['code'] = -1
            ctx['msg'] = '购买不能小于一'
        elif int(nums) > food.stock:
            ctx['code'] = -1
            ctx['msg'] = '购买数量不能大于现有数量'
        elif not Food.query.get(shop_id):
            ctx['code'] = -1
            ctx['msg'] = '没有这个商品'
        else:
            try:
                if membercart:
                    membercart.quantity = int(membercart.quantity) + int(nums)
                    db.session.add(membercart)
                    db.session.commit()
                else:
                    membercart = MemberCart()
                    membercart.member_id = member.id
                    membercart.food_id = shop_id
                    membercart.quantity = nums
                    db.session.add(membercart)
                    db.session.commit()
            except Exception as e:
                ctx['code'] = -1
                ctx['msg'] = '参数不合法'
                return jsonify(ctx)

    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数不合法'
    return jsonify(ctx)


@api.route('/getlist', methods=['POST'])
def get_list():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    token = request.headers.get('token')
    uid, token = token.split("#")
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member)
    membercarts = MemberCart.query.filter_by(member_id=uid).all()
    car_list = []
    totalPrice = 0
    for membercart in membercarts:
        food = Food.query.get(membercart.food_id)
        temp = {}
        temp['id'] = membercart.id
        temp['food_id'] = membercart.food_id
        temp['pic_url'] = get_img_abs(food.main_image)
        temp['name'] = food.name
        temp['price'] = float(food.price)
        temp['activate'] = True  # 是否选中
        temp['number'] = membercart.quantity
        car_list.append(temp)
        totalPrice += int(membercart.quantity) * round(food.price, 2)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    # ctx['totalPrice'] = str(totalPrice)
    ctx['data']['list'] = car_list
    ctx['data']['totalPrice'] = str(totalPrice)
    return jsonify(ctx)


# 对商品执行加操作
@api.route('/edit', methods=['POST'])
def plus():
    ctx = {
        'code': 1,
        'msg': '',
        'data': {}
    }
    id, token = request.headers.get('Token').split('#')
    member = Member.query.get(id)
    food_id = request.form.get('food_id')
    try:
        number = int(request.form.get('number'))
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数不合法'
        return jsonify(ctx)
    membercart = MemberCart.query.filter_by(food_id=food_id, member_id=member.id).first()
    if not member:
        ctx['code'] = -1
        ctx['msg'] = '购物车不存在'
        return jsonify(ctx)
    food = Food.query.get(food_id)
    if not food:
        ctx['code'] = -1
        ctx['msg'] = '食品不存在'
        return jsonify(ctx)
    token1 = MemberService.geneAuthCode(member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token失败'
        return jsonify(ctx)

    membercart.quantity = membercart.quantity + number
    if (
            number != 1 and number != -1) or number > membercart.quantity or membercart.quantity > 10 or membercart.quantity < 0:
        ctx['code'] = -1
        ctx['msg'] = '参数不合法'
        return jsonify(ctx)

    db.session.add(membercart)
    db.session.commit()
    return jsonify(ctx)


@api.route('/del', methods=['POST'])
def delete():
    ctx = {
        'code': 1,
        'msg': '',
        'data': {}
    }
    id, token = request.headers.get('Token').split('#')
    member = Member.query.get(id)
    token1 = MemberService.geneAuthCode(member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token失败'
        return jsonify(ctx)
    ids = request.form.get('ids')
    for id in loads(ids):
        membercar = MemberCart.query.filter_by(id=id).first()
        db.session.delete(membercar)
        db.session.commit()
    return jsonify(ctx)
