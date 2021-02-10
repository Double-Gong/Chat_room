from flask import Blueprint
anonymous_room=Blueprint('anonymous_room',__name__,template_folder='templates')
from .views import *