from flask import Flask

from App.ext import init_ext
from App.settings import envs
from App.view import init_view


def create_app(env):
    app = Flask(__name__)
    #初始化配置文件
    app.config.from_object(envs.get(env))
    # 初始化视图
    init_view(app)
    # 初始化第三方插件
    init_ext(app)

    return app