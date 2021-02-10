from apps import db
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(128))
    # is_online = db.Column(db.Boolean,default=False)
    message = db.relationship('Message', back_populates='author', cascade='all')
    rooms = db.relationship('Room', secondary=lambda: User_to_Room.__table__, back_populates='member')


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1000), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship(User, back_populates='message')
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='messages')

class off_line_Message(db.Model):
    __tablename__ = 'off_line_message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =db.Column(db.String(256))
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    is_anonymous=db.Column(db.Boolean,default=False)
    member = db.relationship(User,secondary=lambda: User_to_Room.__table__, back_populates='rooms')
    messages = db.relationship('Message', back_populates='room')
    off_line_messages = db.relationship('off_line_Message', backref='room')


class User_to_Room(db.Model):
    __tablename__ = 'user_to_room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
