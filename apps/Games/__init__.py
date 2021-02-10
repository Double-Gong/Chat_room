from flask import Blueprint
easy_game=Blueprint('game',__name__,template_folder='templates')
from .views import *