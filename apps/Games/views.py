from apps.Games import easy_game
from flask import render_template,url_for
from flask_login import login_required

@easy_game.route('/', methods=['GET', 'POST'], endpoint='index')
@login_required
def game():
    return render_template('games/game.html')

@easy_game.route('/game2048',methods=['GET'],endpoint='game2048')
@login_required
def game_2048():
    return render_template('games/game_2048.html')
@easy_game.route('/picture_puzzle',methods=['GET'],endpoint='picture_puzzle')
def picture_puzzle():
    return render_template('games/picture_puzzle.html')