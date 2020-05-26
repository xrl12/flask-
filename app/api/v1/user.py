import requests

from flask import request, current_app, jsonify

from app.libs.redprint import RedPrint
from app.models.user import Member, OauthMemberBind, db
from app.service.member_service import MemberService

api = RedPrint(name='users', description='用户模型')  # 传入两个参数，一个是路由，一个是对红图的描述


@api.route('/login', methods=['POST'])
def user():
    ctx = {
        'code': '1',
        'msg': 'OK',
        'data': {}
    }
    code = request.form.get('code')
    gender = request.form.get('gender')
    nickname = request.form.get('nickName')
    avatarurl = request.form.get('avatarUrl')
    openid = MemberService.getOpenid(code=code)

    if not openid:
        ctx['code'] = -1
        ctx['msg'] = '获取openid失败'
        return jsonify(ctx)
    print('----------------------------{}'.format(openid))
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=openid).first()
    if not oauthmemberbind:
        try:
            member = Member()
            member.gender = gender
            member.nickname = nickname
            member.salt = MemberService.getSalt()
            member.avatar = avatarurl
            db.session.add(member)
            db.session.commit()
            oauthmemberbind = OauthMemberBind()
            oauthmemberbind.openid = openid
            oauthmemberbind.client_type = 'weixin'
            oauthmemberbind.type = 1
            oauthmemberbind.member_id = member.id
            db.session.add(oauthmemberbind)
            db.session.commit()
        except Exception as e:
            pass
    member = oauthmemberbind.member
    geneAuthCode = MemberService.geneAuthCode(member)
    ctx['data']['token'] = '%s#%s' % (member.id, geneAuthCode)
    return jsonify(ctx)


@api.route('/checklogin', methods=['POST', 'GET'])
def checklogin():
    ctx = {
        'code': '1',
        'msg': 'OK',
        'data': {}
    }
    code = request.form.get('code')
    openid = MemberService.getOpenid(code=code)
    if not openid:
        ctx['code'] = -1
        ctx['msg'] = '获取openid失败'
        return jsonify(ctx)
    oauthmemberbind = OauthMemberBind.query.filter_by(openid=openid).first()
    if not oauthmemberbind:
        ctx['code'] = -1
        ctx['msg'] = '没有用户信息'
    member = oauthmemberbind.member
    geneAuthCode = MemberService.geneAuthCode(member)
    ctx['data']['token'] = '%s#%s' % (member.id, geneAuthCode)
    return jsonify(ctx)
