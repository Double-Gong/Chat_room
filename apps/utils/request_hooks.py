from app_run import app
from flask_login import current_user
from flask import request,session
import functools



from flask_wtf.csrf import generate_csrf
# 调用函数生成 csrf_token
@app.after_request
def after_request(response):
    # 调用函数生成 csrf_token
    csrf_token = generate_csrf()
    # 通过 cookie 将值传给前端
    response.set_cookie("csrf_token", csrf_token)
    return response

@app.before_request
def before_request():
    session.permanent = True
    return None

# def authenticated_only(f):
#     @functools.wraps(f)
#     def wrapped(*args, **kwargs):
#         if current_user.is_authenticated:
#             disconnect()
#         else:
#             return f(*args, **kwargs)
#     return wrapped

