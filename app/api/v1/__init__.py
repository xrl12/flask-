from flask import Blueprint
from . import user
from . import banner


def createBluePrint():
    dp = Blueprint(name='api', import_name=__name__,url_prefix='/api/v1')
    user.api.register(dp)  # 把红d图的注册的路由交给蓝图
    banner.api.register(dp)
    return dp
