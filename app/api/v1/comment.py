from flask import request, jsonify

from app.models.comment import MemberComment
from app.models.order import PayOrder
from app.service.member_service import MemberService
from app.models.user import Member
from app.libs.redprint import RedPrint
from app import db

api = RedPrint('/comment', description='评论')


@api.route('/add', methods=['POST'])
def add():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }

    token = request.headers.get('token')

    try:
        uid, token = token.split('#')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '没有token'
        return jsonify(ctx)
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)

    # 获取前端传来的参数,并判断是否合法
    try:
        score = int(request.form.get('score'))
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '参数不合法'
        return jsonify(ctx)
    order_number = request.form.get('order_number')
    content = request.form.get('content')
    payorder = PayOrder.query.filter_by(order_sn=order_number).first()

    print(score, order_number, content)
    if score > 10 or score < 0:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
        return jsonify(ctx)
    elif not content or not str(content).strip():
        ctx['code'] = -1
        ctx['msg'] = '内容不能为空'
        return jsonify(ctx)
    if not payorder:
        ctx['code'] = -1
        ctx['msg'] = '参数错误'
        return jsonify(ctx)
    try:
        membercomment = MemberComment()
        membercomment.content = content
        membercomment.member_id = member.id
        membercomment.order_id = payorder.id
        db.session.add(membercomment)
        db.session.commit()
        payorder.status = 1
        db.session.add(payorder)
        db.session.commit()

    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '未知错误'
        return jsonify(ctx)
    return jsonify(ctx)


@api.route('/list')
def list():
    ctx = {
        'code': 1,
        'msg': 'ok',
        'data': {}
    }

    token = request.headers.get('token')

    try:
        uid, token = token.split('#')
    except Exception as e:
        ctx['code'] = -1
        ctx['msg'] = '没有token'
        return jsonify(ctx)
    member = Member.query.get(uid)
    token1 = MemberService.geneAuthCode(member=member)
    if token != token1:
        ctx['code'] = -1
        ctx['msg'] = 'token错误'
        return jsonify(ctx)

    """
        前端需要的数据类型
        {
            date: "2018-07-01 22:30:23",
            order_number: "20180701223023001",
            content: "记得周六发货",
        },
    """
    membercomments = MemberComment.query.filter_by(member_id=member.id).all()
    comment = [{'date': membercomment.create_time, 'order_number': PayOrder.query.get(membercomment.order_id).order_sn,
                'content': membercomment.content
                } for
               membercomment in membercomments]
    ctx['data']['list'] = comment
    print(ctx)
    return jsonify(ctx)
