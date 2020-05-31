from flask import jsonify, request

from app import db
from app.libs.redprint import RedPrint
from app.models.user import Member
from app.service.member_service import MemberService
from app.models.address import MemberAddress

api = RedPrint('/address', description='地址')


@api.route('/add', methods=['POST'])
def add():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    try:
        token = request.headers.get('token')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '没有token'
        return jsonify(ctx)
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
    # ------------------------------------------------------
    # 获取前端传来的参数
    name = request.form.get('name')
    phone = request.form.get('phone')
    detail_address = request.form.get('detail_address')
    province = request.form.get('province')
    province_str = request.form.get('province_str')
    city = request.form.get('city')
    city_str = request.form.get('city_str')
    area = str(request.form.get('area'))
    area_str = request.form.get('area_str')

    # 判断是否为空
    if not name or not phone or not detail_address or not province or not province_str or not city or not city_str:
        ctx['code'] = -1
        ctx['msg'] = '数据不能为空'
        return jsonify(ctx)

    """
    开始添加数据
    判断这个用户是否已经有了默认地址，如果没有就将地址为默认地址，有就不设置
    """
    memberaddress = MemberAddress()
    memberaddress.member_id = member.id
    memberaddress.nickname = name
    memberaddress.mobile = phone
    memberaddress.address = detail_address
    memberaddress.province_id = province
    memberaddress.province_str = province_str
    memberaddress.city_id = city
    memberaddress.city_str = city_str
    memberaddress.area_id = area
    memberaddress.area_str = area_str

    ma = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()

    if ma:
        memberaddress.is_default = 0
    else:
        memberaddress.is_default = 1
    db.session.add(memberaddress)
    db.session.commit()

    return jsonify(ctx)


@api.route('/list', methods=['GET'])
def list():
    ctx = {
        'code': 1,
        'msg': 'OK',
        'data': {}
    }
    try:
        token = request.headers.get('token')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '没有token'
        return jsonify(ctx)
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

    # 获取数据
    """"
    需要的数据结构
    {
        id: 1,
        name: "test1",
        mobile: "12345678901",
        detail: "上海市浦东新区XX",
        isDefault: 1
    }
    """

    memberaddresses = MemberAddress.query.filter_by(member_id=member.id).all()
    addressList = [
        {'id': memberaddress.id, 'name': memberaddress.nickname, 'mobile': memberaddress.mobile,
         'detail': memberaddress.province_str + memberaddress.city_str + memberaddress.area_str + memberaddress.address,
         'isDefault': memberaddress.is_default} for memberaddress in memberaddresses]
    ctx['data']['addressList'] = addressList
    return jsonify(ctx)
