from apps import create_app,cache,redis_client
from flask_socketio import SocketIO
from flask import request,session
app = create_app()

socketio = SocketIO(app,async_mode='eventlet'
                    # ,logger=True, engineio_logger=True
                    )


# 各功能模块导入
from apps.utils.request_hooks import *
from apps.Anonymous_room.anonynous_socketio import *
from apps.RealName_room.realname_socketio import *
from apps.Games.game_2048 import *
from apps.Games.picture_puzzle import *

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port='8989')
