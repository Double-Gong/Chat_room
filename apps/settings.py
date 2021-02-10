import datetime


class RoomsConfig():
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:123456@127.0.0.1:3306/Chat_room'
    SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
    SECRET_KEY = 'chat_room'
    CACHE_TYPE = 'redis'  # 缓存类型
    CACHE_REDIS_URL = 'redis://@localhost:6379/2'
    REDIS_URL = 'redis://@localhost:6379/3'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=15)
