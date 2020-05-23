from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel
from flask_login import LoginManager
from config import CONFIG_MAPPING

db = SQLAlchemy()

# 登录管理后台
login_manage = LoginManager()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPING[config])
    db.init_app(app=app)
    from app.api.v1 import createBluePrint
    app.register_blueprint(createBluePrint())  # 注册蓝图

    # 添加管理后台
    from .models.food import Food, Category
    from app.admin.modelview import FModelview
    admin = Admin(app, name='管理后台', template_mode='bootstrap3', base_template='admin/mybase.html')  # 此行新加
    admin.add_view(FModelview(Food, db.session, name='食品'))  # 第一个传入的是模型类，第二个传入的是db_session，第三个传入的是网页的title
    admin.add_view(ModelView(Category, db.session, name='食品分类'))
    # 对管理后台进行汉化
    babel = Babel(app=app)

    login_manage.init_app(app=app)

    # 后台管理实现登录或者注册才可以进行访问
    from app.admin import admin_page
    app.register_blueprint(admin_page, url_prefix='/admin')

    return app
