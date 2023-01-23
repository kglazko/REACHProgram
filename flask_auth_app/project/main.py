from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import CurrentGame
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/game')
@login_required
def game():
	correct_answer = "1234"
	status = "not won"
	attempt = 0
	new_game = CurrentGame(correct_answer=correct_answer, status=status, attempt=attempt)

	db.session.add(new_game)
	db.session.commit()
	return render_template('game.html', name=current_user.name)

@main.route('/game', methods=['POST'])
def game_post():
    guess = request.form.get('guess')
    user_email = current_user.email

    current_game = CurrentGame.query.filter_by(correct_answer = "1234").first()
    current_game.attempt += 1
    db.session.commit()
    if guess == "1234":
        print("fuck")
        print(user_email)

        return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt))
    
    return redirect(url_for('main.game'))
