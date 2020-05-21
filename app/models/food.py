from .BaseModel import BaseModel
from app import db


class Food(BaseModel, db):
    __tablename__ = 'tab_food'
    order = db.Column(db.Integer, default=0, comment='排序')
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    name = db.Column(db.String(32), nullable=False, comment='食品名字')
    price = db.Column(db.Integer, nullable=False, comment='价钱')
    min_price = db.Column(db.Integer, nullable=True, comment='最低价格,可以不写')
    img_url = db.Column(db.String(32), nullable=False, comment='图片的地址')
    detail = db.Column(db.String(32), nullable=True, comment='食品详情')
    is_delete = db.Column(db.Boolean, default=False, comment='是否删除')
    cat_id = db.Column(db.Integer, db.ForeignKey('tab_cat.id'),comment='分类id',nullable=False)
    banner_Id = db.Column(db.Integer, db.ForeignKey('tab_banner.id'),comment='轮播图id',nullable=True)


class Category(BaseModel, db):
    __tablename__ = 'tab_cat'
    id = db.Column(db.Integer, primary_key=True, comment='主键')
    order = db.Column(db.Integer, default=0, comment='排序')
    name = db.Column(db.String(32), nullable=False, comment='分类名字')
    is_delete = db.Column(db.Boolean, default=False, comment='是否删除，默认不删除')
    foods = db.relationship(Food, backref='category')


class Banner(BaseModel, db):
    __tablename__ = 'tab_banner'
    id = db.Column(db.Integer, primary_key=True, comment='id')
    order = db.Column(db.Integer, default=0, comment='排序')
    img_address = db.Column(db.String(32), nullable=False, comment='图片地址')
    is_delete = db.Column(db.Boolean, default=False, comment='是否删除,默认不删除')
    food = db.relationship(Food, backref='banner', uselist=False)
