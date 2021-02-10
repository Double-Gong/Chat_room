from app_run import socketio, cache, app, redis_client
from flask import request, session, redirect, url_for
from flask_login import current_user, logout_user, UserMixin, AnonymousUserMixin
from flask_socketio import emit, join_room, leave_room, rooms, Namespace, disconnect
from apps.auth.models import *
import time
import eventlet


class anonymous_chat(Namespace):
    is_anonymous = True

    def on_connect(self):
        # 通过ip辨识用户身份
        print('-' * 15, '>on chat connect<', '-' * 15)
        if isinstance(current_user._get_current_object(), AnonymousUserMixin):
            disconnect(request.sid)
        else:
            self.room_select()

    def on_send_message(self, data):
        print('-' * 15, '>on_send_message<', '-' * 15)
        print(data)
        self._handle_message(data)
        response = {'room_id': data['room_id'],
                    'message': data['message'],
                    'author': '匿名用户' + str(current_user.id) if self.is_anonymous else current_user.username}
        emit('on_receive_message', response, room=data['room_id'], skip_sid=request.sid)

    def on_click_room(self, data):
        print('-' * 15, '>on_click_room<', '-' * 15)
        message_list = Message.query.filter_by(room_id=data['room_id']).order_by(Message.id.desc()).limit(10).all()
        messages = [
            {'author': '匿名用户' + str(item.author.id) if self.is_anonymous else item.author.username,
             'message': str(item.content)}
            for item in message_list[-1::-1]]
        room_name = Room.query.filter_by(id=data['room_id']).first().name
        emit('on_show_message', {'room_name': room_name, 'msg_list': messages})
        print(messages)

    def on_message_confirm(self, data):
        print('-' * 15, '>on_message_confirm<', '-' * 15)
        print(data)
        redis_client.hset('off_line_message', 'room:{}|user:{}'.format(data['room_id'], current_user.id), 0)

    def on_room_create(self, data):
        print('-' * 15, '>on_room_create<', '-' * 15)
        print(data)
        new_room = Room(name=data['room_name'], is_anonymous=self.is_anonymous)
        new_room.member.append(current_user)
        db.session.add(new_room)
        db.session.commit()
        join_room(str(new_room.id))
        emit('join_new_room', {'room_id': new_room.id, 'room_name': new_room.name, 'message_count': 0})

    def on_room_select(self, data):
        print('-' * 15, '>on_room_select<', '-' * 15)
        print(data)
        target_room = Room.query.filter_by(id=data['room_id'], is_anonymous=self.is_anonymous).first()
        if target_room:
            if current_user not in target_room.member:
                target_room.member.append(current_user)
                db.session.commit()
                join_room(str(target_room.id))
                emit('join_new_room', {'room_id': target_room.id, 'room_name': target_room.name, 'message_count': 0})
            else:
                emit('on_alert_message', {'msg': '您已经在房间{}中'.format(target_room.name)})
        else:
            emit('on_alert_message', {'msg': '请输入存在的房间号'})

    def room_select(self):
        room_list = []
        for item in current_user.rooms:
            if item.is_anonymous == self.is_anonymous:
                join_room(str(item.id))
                room_list.append(
                    {'room_id': item.id,
                     'room_name': item.name,
                     'message_count': str(redis_client.hget('off_line_message',
                                                            'room:{}|user:{}'.format(item.id, current_user.id)) or 0),
                     'last_time': str(item.messages[-1].create_time) if item.messages else '0000-00-00 00:00:00'})
        print(rooms())
        room_list.sort(key=lambda item: item['last_time'], reverse=True)
        print(room_list)
        emit('on_rooms', {'room_list': room_list})

    @staticmethod
    def _handle_message(data):
        current_room = Room.query.filter_by(id=data['room_id']).first()
        print('---------->存入数据<----------', type(data['message']), data['message'])
        new_message = Message(content=str(data['message']), author=current_user, room_id=data['room_id'])
        db.session.add(new_message)
        db.session.commit()
        for user in current_room.member:
            if user != current_user:
                redis_client.hsetnx('off_line_message', 'room:{}|user:{}'.format(data['room_id'], user.id), 0)
                redis_client.hincrby('off_line_message', 'room:{}|user:{}'.format(data['room_id'], user.id), 1)


socketio.on_namespace(anonymous_chat('/anonymous_chat'))
