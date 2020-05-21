from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import CONFIG_MAPPING

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(CONFIG_MAPPING[config])
    db.init_app(app=app)
    from app.api.v1 import createBluePrint
    app.register_blueprint(createBluePrint())  # 注册蓝图
    return app
