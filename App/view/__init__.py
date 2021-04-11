from .log import blueEnum
from .firs_blue import blue
from .poc_blue import blue_poc


def init_view(app):
    app.register_blueprint(blue)
    app.register_blueprint(blue_poc)
    app.register_blueprint(blueEnum)