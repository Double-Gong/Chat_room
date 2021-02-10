from flask import Flask,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_caching import Cache
from flask_redis import FlaskRedis

db = SQLAlchemy()
login_manager = LoginManager()
cache=Cache()
redis_client =FlaskRedis()

from apps.auth.models import *
from apps.Anonymous_room import anonymous_room
from apps.auth import auth
from apps.Games import easy_game



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.id==user_id).first()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


def create_app():
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(anonymous_room,url_prefix='/anonymous_room')
    app.register_blueprint(easy_game,url_prefix='/game')
    app.register_blueprint(auth)

    # 添加配置
    app.config.from_object('apps.settings.RoomsConfig')
    # 读取配置
    db.init_app(app)
    cache.init_app(app,config={'CACHE_TYPE': 'redis',  # 缓存类型
        'CACHE_REDIS_URL': 'redis://@localhost:6379/2'})
    redis_client.init_app(app,decode_responses=True) # redis返回数据decode
    login_manager.init_app(app)
    CSRFProtect(app)

    return app
