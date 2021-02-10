from flask_socketio import Namespace
from app_run import socketio, cache, redis_client
import numpy as np
from flask_socketio import emit
import json
from flask_login import current_user
from flask import request
from PIL import Image
import base64
from io import BytesIO


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class Picture_puzzle(Namespace):
    def move(self,direction):
        for i in range(len(self.game_img_list)):
            for j in range(len(self.game_img_list[i])):
                try:
                    if self.game_img_list[i][j]['value']=='{}-{}'.format(self.game_level-1,self.game_level-1):
                        if direction=='left':
                            self.game_img_list[i][j], self.game_img_list[i][j + 1] = self.game_img_list[i][j + 1],self.game_img_list[i][j]
                        elif direction=='right':
                            if j==0:
                                return
                            self.game_img_list[i][j],self.game_img_list[i][j-1]=self.game_img_list[i][j-1],self.game_img_list[i][j]
                        elif direction=='up':
                            self.game_img_list[i][j], self.game_img_list[i+1][j] = self.game_img_list[i+1][j],self.game_img_list[i][j]
                        elif direction=='down':
                            if i == 0:
                                return
                            self.game_img_list[i][j], self.game_img_list[i - 1][j] = self.game_img_list[i - 1][j],self.game_img_list[i][j]
                        self.game_steps+=1
                        return
                except Exception as e:
                    print(str(e))
                    return


    def over(self):
        for i in range(len(self.game_img_list)):
            for j in range(len(self.game_img_list[i])):
                if self.game_img_list[i][j]['value'] != '{}-{}'.format(i,j):
                    return False
        return True

    def after_operate(self):
        game_data = json.dumps(self.game_img_list, cls=MyEncoder)
        emit('receive_img', {'img_data': game_data, 'game_steps': self.game_steps})
        if self.over():
            print('-' * 25, 'game over', '*' * 25)
            emit('game_over')

    def on_left(self):
        self.move('left')
        self.after_operate()

    def on_right(self):
        self.move('right')
        self.after_operate()

    def on_up(self):
        self.move('up')
        self.after_operate()

    def on_down(self):
        self.move('down')
        self.after_operate()

    def on_over(self):
        print('------------>is over<------------')
        self.game_img_list = []
        self.game_steps = 0

    def on_start_game(self, data):
        print('*' * 25, 'start_puzzle', '*' * 25)
        game_img = Image.open(BytesIO(data['game_img']))
        white_block=Image.open('apps/static/white.png')
        self.game_level = int(data['game_level'])
        w, h = game_img.size
        b = min(w, h)
        step = int(b / self.game_level)
        self.game_img_list = []
        for i in range(self.game_level):
            for j in range(self.game_level):
                img_temp = game_img.crop((j * step, i * step, (j + 1) * step, (i + 1) * step))
                f = BytesIO()
                if i==j==self.game_level-1:
                    print(i,j)
                    white_block.save(f,'png')
                else:
                    img_temp.save(f, 'jpeg')
                img_temp_data = f.getvalue()
                img_data = base64.b64encode(img_temp_data).decode()
                self.game_img_list.append({'value': '{}-{}'.format(i, j), 'img': img_data})
        self.game_img_list=np.random.choice(self.game_img_list, replace=False, size=self.game_level ** 2).reshape(self.game_level, self.game_level).tolist()
        self.game_steps=0
        emit('receive_img', {'img_data': json.dumps(self.game_img_list)})


socketio.on_namespace(Picture_puzzle('/picture_puzzle'))
