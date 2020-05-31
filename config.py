class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/db_10_waimai'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False

    # 对管理后台进行汉化
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    # 小程序配置
    APPSECRET = '31136dd4dea8551834b76a75f4a07ad6'
    APPID = 'wxe0632a1e3ec5281f'

    # 设置商户密钥
    MERCHANT_KEY = 'd525c5cab569476bbf980fd982097841'
    # 设置商户的id
    MCH_ID = 123123123

    # session配置
    SECRET_KEY = 'sjdfasfsadfadksfjasdl'

    # 返回图片的绝对地址
    DOMAIN = 'http://127.0.0.1:5000/static/'

    # 支付完成后设置一个回调地址
    NOTIFY_URL = 'http://127.0.0.1:5000/order/callback'

    # 验证图片的合法性
    IMG_FORMAT = ['png', 'jpeg', 'jpg', 'gif']


class Product(Config):  # 线上的
    DEBUG = False


class Dev(Config):  # 线下的
    DEBUG = True


CONFIG_MAPPING = {
    'dev': Dev,
    'pro': property
}
