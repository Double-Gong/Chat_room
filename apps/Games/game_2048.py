from flask_socketio import Namespace
from app_run import socketio, cache
import numpy as np
from flask_socketio import emit
import json
from flask import request


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


class Game_2048(Namespace):
    choice = [0, 2, 4]
    choice_p = [0.65, 0.3, 0.05]

    def start_game(self):
        self.game_list = []
        self.game_score = 0
        self.change_signal = False
        for i in range(4):
            self.game_list.append(list(np.random.choice(self.choice, 4, p=self.choice_p)))

    def remove_zero(self):
        cache.set(str(request.sid) + "last_game_list", self.game_list)
        for i in range(len(self.game_list)):
            for j in range(len(self.game_list[i]) - 1, -1, -1):
                if self.game_list[i][j] == 0:
                    self.game_list[i].pop(j)
                    self.game_list[i].append(0)
        if cache.get(str(request.sid) + "last_game_list") != self.game_list:
            self.change_signal = True

    def left(self):
        self.remove_zero()
        for i in range(len(self.game_list)):
            for j in range(len(self.game_list[i]) - 1):
                if self.game_list[i][j] == 0:
                    continue
                if self.game_list[i][j] == self.game_list[i][j + 1]:
                    self.game_list[i][j] += self.game_list[i][j]
                    self.game_score += int(self.game_list[i][j]) * 2
                    self.change_signal = True
                    self.game_list[i].pop(j + 1)
                    self.game_list[i].append(0)
        if self.change_signal:
            for i in range(len(self.game_list)):
                if self.game_list[i][-1] == 0:
                    self.game_list[i][-1] = np.random.choice(self.choice, 1, p=self.choice_p)[0]

    def reversed_list(self):
        self.game_list = np.array(self.game_list, dtype='int64')[:, ::-1].tolist()

    def transport_list(self):
        self.game_list = np.array(self.game_list, dtype='int64').T.tolist()

    def right(self):
        self.reversed_list()
        self.left()
        self.reversed_list()

    def up(self):
        self.transport_list()
        self.left()
        self.transport_list()

    def down(self):
        self.transport_list()
        self.reversed_list()
        self.left()
        self.reversed_list()
        self.transport_list()

    def over(self):
        over_signal = True
        for i in range(len(self.game_list)):
            for j in range(len(self.game_list[i])):
                if self.game_list[i][j] == 0:
                    over_signal = False
                    return over_signal
                try:
                    if self.game_list[i][j] == self.game_list[i][j + 1]:
                        over_signal = False
                        return over_signal
                except:
                    continue
                try:
                    if self.game_list[i][j] == self.game_list[i + 1][j]:
                        over_signal = False
                        return over_signal
                except:
                    continue
        return over_signal

    def after_operate(self, direction):
        game_data = json.dumps(self.game_list, cls=MyEncoder)
        emit('receive_data', {'game_data': game_data, 'game_score': self.game_score})
        if self.over():
            print('-' * 25, 'game over', '*' * 25)
            emit('game_over')
        self.change_signal = False
        print('*' * 25, self.game_list)

    def on_left(self):
        self.left()
        self.after_operate('left')

    def on_right(self):
        self.right()
        self.after_operate('right')

    def on_up(self):
        self.up()
        self.after_operate('up')

    def on_down(self):
        self.down()
        self.after_operate('down')

    def on_over(self):
        print('------------>is over<------------')
        self.game_list = []
        self.change_signal = False

    def on_start(self):
        self.start_game()
        game_data = json.dumps(self.game_list, cls=MyEncoder)
        emit('receive_data', {'game_data': game_data})


socketio.on_namespace(Game_2048('/game2048'))
