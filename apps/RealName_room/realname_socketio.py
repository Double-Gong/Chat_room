from apps.Anonymous_room.anonynous_socketio import anonymous_chat

from app_run import socketio,cache,app,redis_client
from flask import request,session,redirect,url_for
from flask_login import current_user, logout_user,UserMixin,AnonymousUserMixin
from flask_socketio import emit,join_room,leave_room, rooms, Namespace,disconnect
from apps.auth.models import *
import functools

class realname_chat(anonymous_chat):
    is_anonymous = False

socketio.on_namespace(realname_chat('/realname_chat'))
