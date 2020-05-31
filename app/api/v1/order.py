import json

from flask import request, jsonify, current_app

from app.libs.redprint import RedPrint
from app.utils.common import get_img_abs
from app.service.member_service import MemberService

from app import db
from app.utils.common import geneOrderSn
from app.service.WeChatService import WeChatService

from app.models.order import PayOrder, PayOrderItem
from app.models.food import Food
from app.models.user import Member, OauthMemberBind
from app.models.cars import MemberCart
from app.models.address import MemberAddress

api = RedPrint('/order', description='订单')


@api.route('/info', methods=['POST'])
def info():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }
    try:
        token = request.headers.get('token')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '没有token'
        return jsonify(ctx)

    uid, token = token.split('#')
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    foods_id = request.form.get('ids')
    try:
        ids = eval(foods_id)
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
        return jsonify(ctx)
    pay_price = 0
    food_list = []
    for id in ids:
        temp = {}
        food = Food.query.get(id)
        membercar = MemberCart.query.filter_by(member_id=member.id, food_id=food.id).first()
        temp['id'] = food.id
        temp['name'] = food.name
        temp['price'] = str(food.price)
        temp['pic_url'] = get_img_abs(food.main_image)
        temp['number'] = membercar.quantity
        food_list.append(temp)
        pay_price += membercar.quantity * food.price

    memberaddress = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()
    if memberaddress:
        default_address = {
            'id': memberaddress.id,
            'name': memberaddress.nickname,
            'mobile': memberaddress.mobile,
            'detail': memberaddress.showAddress
        }
    else:
        default_address = {}

    yun_price = 0
    pay_price = pay_price
    total_price = pay_price + yun_price

    ctx['data']['food'] = food_list
    ctx['data']['default_address'] = default_address
    ctx['data']['yun_price'] = str(yun_price)
    ctx['data']['pay_price'] = str(pay_price)
    ctx['data']['total_price'] = str(total_price)
    return jsonify(ctx)


@api.route('/create', methods=['POST'])
def create():
    try:
        ctx = {
            'code': 1,
            'msg': 'ok',
            'data': {}
        }

        # 进行token判断
        token = request.headers.get('token')
        try:
            uid, token = token.split('#')
        except Exception as e:
            ctx['code'] = -1
            ctx['msg'] = 'token错误'
            return jsonify(ctx)
        member = Member.query.get(uid)
        token1 = MemberService.geneAuthCode(member=member)
        if token != token1:
            ctx['code'] = -1
            ctx['msg'] = 'token错误'
            return jsonify(ctx)
        # 获取从前端传来的值
        ids = request.form.get('ids')
        note = request.form.get("note")
        address_id = request.form.get("address_id")
        ids = json.loads(ids)
        # 生成订单表
        total_price = 0
        yun_price = 0
        pay_price = 0
        for id in ids:
            temp = {}
            membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
            food = Food.query.get(id)
            pay_price += membercart.quantity * food.price
        total_price = pay_price + yun_price

        memberaddress = MemberAddress.query.get(address_id)
        if not memberaddress:
            ctx['code'] = -1
            ctx['msg'] = '参数不合法'
            return jsonify(ctx)
        payorder = PayOrder()
        payorder.order_sn = geneOrderSn(PayOrder)
        payorder.total_price = total_price  # 商品的价格和运费
        payorder.yun_price = 0
        payorder.pay_price = pay_price  # 购买商品的价格
        payorder.note = note
        payorder.status = -8
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.nickname + memberaddress.mobile + memberaddress.showAddress
        payorder.member_id = member.id
        db.session.add(payorder)
        # ----------------------------------------------------------------------------------------------------------------------------------------->
        foods = db.session.query(Food).filter(Food.id.in_(ids)).with_for_update().all()  # 上悲观锁
        temp_stock = {}
        for food in foods:
            temp_stock[food.id] = food.stock

        for id in ids:
            membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
            if membercart.quantity > temp_stock[id]:  # 引用分控
                ctx['code'] = -1
                ctx['msg'] = '库存不足'
                return jsonify(ctx)
            food = db.session.query(Food).filter(Food.id == id).update({
                'stock': temp_stock[id] - membercart.quantity
            })
            if not food:
                ctx['code'] = -1
                ctx['msg'] = '更新失败'
                return jsonify(ctx)
            food = Food.query.get(id)
            payitem = PayOrderItem()
            payitem.quantity = membercart.quantity
            payitem.price = food.price
            payitem.note = note
            payitem.status = 1
            payitem.pay_order_id = payorder.id
            payitem.member_id = member.id
            payitem.food_id = food.id
            db.session.add(payitem)

            # 删除购物车
            db.session.delete(membercart)
        db.session.commit()

    except Exception as e:
        print(e)
        ctx['code'] = -1
        ctx['msg'] = '失败'
        db.session.rollback()

    return jsonify(ctx)


@api.route('/list', methods=['GET'])
def list():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }

    # 进行token判断
    token = request.headers.get('token')
    try:
        uid, token = token.split('#')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    order_list = []
    status = request.args.get('status')
    payorders = PayOrder.query.filter_by(member_id=member.id, status=status).all()
    total_price = 0
    for payoder in payorders:
        temp = {}
        temp['status'] = payoder.status
        temp['date'] = payoder.pay_time
        temp['order_number'] = payoder.order_sn
        temp['note'] = payoder.note
        temp['total_price'] = str(payoder.total_price + total_price)
        temp['goods_list'] = []
        payorderitem = PayOrderItem.query.filter_by(pay_order_id=payoder.id).all()
        for item in payorderitem:
            pic = {}
            food = Food.query.get(item.food_id)
            pic['pic_url'] = get_img_abs(food.main_image)
            temp['goods_list'].append(pic)
        order_list.append(temp)
    ctx['data']['order_list'] = order_list
    return jsonify(ctx)


# 发送支付请求
@api.route('/pay', methods=['POST'])
def pay():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }

    # 进行token判断
    token = request.headers.get('token')
    try:
        uid, token = token.split('#')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)

    # 获取前端传来的参数
    order_sn = request.form.get('order_sn')
    payorder = PayOrder.query.filter_by(order_sn=order_sn).first()
    oauthmemberbind = OauthMemberBind.query.filter_by(member_id=member.id).first()
    # 生成签名
    wechatservice = WeChatService(merchant_key=current_app.config['MERCHANT_KEY'])
    pay_data = {
        'appid': current_app.config['APPID'],  # 小程序id
        'mch_id': current_app.config['MCH_ID'],  # 商户id
        'nonce_str': wechatservice.get_nonce_str(),  # 随机字符串，长度要求在32位以内。
        'body': '订餐',  # 商品描述
        "out_trade_no": payorder.order_sn,  # 商户订单号
        'total_fee': str(payorder.total_price * 100),  # 商品的价格，注意！！单位是分
        'spbill_create_ip': '127.0.0.1',  # 终端ip地址
        'notify_url': current_app.config['NOTIFY_URL'],  # 回调接口
        'trade_type': 'JSAPI',  # 交易类型
        'openid': oauthmemberbind.openid
    }
    # 进行签名
    pay_info = wechatservice.get_pay_info(pay_data)

    # 将支付成功的流水号进行保存起来
    payorder.pay_sn = pay_info
    db.session.add(pay_info)
    db.session.commit()

    ctx['data']['payinfo'] = pay_info
    return jsonify(ctx)


@api.route("/callback", methods=["POST"])
def orderCallback():
    result_data = {
        'return_code': 'SUCCESS',
        'return_msg': 'OK'
    }
    header = {'Content-Type': 'application/xml'}
    target_wechat = WeChatService(merchant_key=current_app.config['PAYKEY'])
    # 解析微信推送过来的xml 支付结果  改成字典
    callback_data = target_wechat.xml_to_dict(request.data)

    # 取出这里面sign
    sign = callback_data['sign']

    # 在pop掉sign
    callback_data.pop('sign')

    # 在把这个字典进行签名 返回一个sign
    gene_sign = target_wechat.create_sign(callback_data)  # 在加密
    # 如果取出的sign和加密后的sign不一样
    if sign != gene_sign:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 如果返回的不等于成功
    if callback_data['result_code'] != 'SUCCESS':
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header
    # 订单号取出来
    order_sn = callback_data['out_trade_no']

    # 根据订单查这个订单的信息
    pay_order_info = PayOrder.query.filter_by(order_sn=order_sn).first()
    if not pay_order_info:
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    # 如果付款的金额和推送过来的支付金额不一样
    if int(pay_order_info.total_price * 100) != int(callback_data['total_fee']):
        result_data['return_code'] = result_data['return_msg'] = 'FAIL'
        return target_wechat.dict_to_xml(result_data), header

    if pay_order_info.status == -8:
        return target_wechat.dict_to_xml(result_data), header

    # 把订单更新待发货
    # OrderService.orderSuccess(pay_order_id=pay_order_info.id, params={"pay_sn": callback_data['transaction_id']})
    # 把支付结果存起来
    return target_wechat.dict_to_xml(result_data), header


@api.route('/cancel', methods=['POST'])
def cancel():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }

    # 进行token判断
    token = request.headers.get('token')
    try:
        uid, token = token.split('#')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)

    '''
    获取前端传来的值
    '''
    order_sn = request.form.get('order_sn')
    payorder = PayOrder.query.filter_by(member_id=member.id, order_sn=order_sn).first()
    if not payorder:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
        return jsonify(ctx)
    payorder.status = 0
    db.session.add(payorder)
    db.session.commit()
    return jsonify(ctx)
