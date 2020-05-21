class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/db_10_waimai'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    # 小程序配置
    APPSECRET = '31136dd4dea8551834b76a75f4a07ad6'
    APPID = 'wxe0632a1e3ec5281f'


class Product(Config):  # 线上的
    DEBUG = False


class Dev(Config):  # 线下的
    DEBUG = True


CONFIG_MAPPING = {
    'dev': Dev,
    'pro': property
}
