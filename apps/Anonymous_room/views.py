from . import anonymous_room
from flask import render_template
from flask import request
from flask_login import login_required

@anonymous_room.route('/',methods=['GET','POST'])
@login_required
def index():
    return render_template('chat.html')