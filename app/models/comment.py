from .BaseModel import BaseModel
from app import db


class MemberComment(db.Model, BaseModel):
    __tablename__ = 'member_comment'
    id = db.Column(db.Integer, primary_key=True, comment='唯一标识')
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False, comment='用户的id')
    order_id = db.Column(db.Integer, db.ForeignKey('pay_order.id'), comment='订单id')
    content = db.Column(db.String(255), nullable=False, comment='评价的内容')
    is_delete = db.Column(db.Boolean,default=False,comment='是否删除')
    position = db.Column(db.Integer,default=0,comment='排序')

