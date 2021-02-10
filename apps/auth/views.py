from apps.auth import auth
from flask import request, render_template, flash, redirect, url_for, session
from apps.utils.forms import *
from apps.auth.models import User, db
from flask_login import login_user, login_required, logout_user, current_user
import hashlib


@auth.route('/login', methods=['GET', 'POST'], endpoint='login')
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        form_data = LoginForm(request.form)
        if form_data.validate():
            password_hash = hashlib.md5(form_data.data['password'].encode('utf-8')).hexdigest()
            user_temp = User.query.filter(User.username == form_data.data['username'],
                                          User.password_hash == password_hash).first()
            if user_temp:
                login_user(user_temp)
                db.session.commit()
                # session['user_id'] = current_user.id
                return redirect(url_for('auth.index'))
            else:
                flash('用户名或密码错误')
        else:
            for error, msg in form_data.errors.items():
                flash(msg[0])
        return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'], endpoint='register')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form_data = RegisterForm(request.form)
        if form_data.validate():
            user_temp = User.query.filter(User.email == form_data.data['email']).first()
            if user_temp:
                flash('用户已存在！')
            else:
                pwd = hashlib.md5(form_data.data['password'].encode('utf-8')).hexdigest()
                pwd_again = hashlib.md5(form_data.data['password_again'].encode('utf-8')).hexdigest()
                if pwd == pwd_again:
                    user_new = User(username=form_data.data['username'], email=form_data.data['email'],
                                    password_hash=pwd)
                    db.session.add(user_new)
                    db.session.commit()
                    db.session.close()
                    login_user(user_new)
                    return redirect(url_for('auth.index'))
                else:
                    flash('两次密码不一致')
        else:
            for error, msg in form_data.errors.items():
                flash(msg[0])
        return redirect(url_for('auth.register'))


@auth.route('/chat', methods=['GET', 'POST'], endpoint='chat')
@login_required
def chat():
    return render_template('auth/chat.html')


@auth.route('/', methods=['GET'], endpoint='index')
@login_required
def index():
    return render_template('auth/index.html')


@login_required
@auth.route('/logout', endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
