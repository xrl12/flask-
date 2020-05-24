from flask import request, jsonify
from app.libs.redprint import RedPrint
from app.models.cars import MemberCart
from app.models.user import Member
from app.models.food import Food
from app import db

api = RedPrint('/cars', description='添加购物车')


@api.route('/addcars', methods=['POST'])
def cars():
    ctx = {
        'code': '1',
        'msg': 'OK',
        'data': {}
    }
    try:
        token = request.form.get('token')
        nums = request.form.get('nums')
        shop_id = request.form.get('id')
        member_id = token.split('#')[0]  # 获取member id
        member = Member.query.get(member_id)
        membercart = MemberCart.query.fiter(MemberCart.member_id == member_id, MemberCart.food_id == shop_id).first()

        if not member:
            ctx['code'] = -1
            ctx['msg'] = '找不到用户'
        elif int(nums) < 1:
            ctx['code'] = -1
            ctx['msg'] = '购买不能小于一'
        elif not Food.query.get(shop_id):
            ctx['code'] = -1
            ctx['msg'] = '没有这个商品'
        try:
            if membercart:
                membercart.quantity = membercart.quantity + nums
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
            pass
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数不合法'
    return jsonify(ctx)
