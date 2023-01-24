import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import CurrentGame, GameAttempt, UserPrefs
from . import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	game_records = CurrentGame.query.filter_by(user_email= current_user.email)
	return render_template('profile.html', name=current_user.name, game_records=game_records)

@main.route('/game_menu')
@login_required
def game_menu():
	game_records = CurrentGame.query.filter_by(user_email= current_user.email)
	return render_template('game_menu.html', name=current_user.name)

@main.route('/game_menu', methods=['POST'])
def game_menu_post():
	difficulty = request.form.get('difficulty')
	print(difficulty)

	user_email = current_user.email

	user = UserPrefs.query.filter_by(user_email=user_email).first() # if this returns a user, then the email already exists in database
	if user:
		user.difficulty = difficulty
		db.session.commit()
	else:
		user = UserPrefs(user_email=user_email, difficulty=difficulty)
		db.session.add(user)
		db.session.commit()

	return redirect(url_for('main.game'))


@main.route('/game')
@login_required
def game():
	# Send a request to the random int API
	difficulty = UserPrefs.query.filter_by(user_email=current_user.email).first().difficulty
	num_diff = num_digits_to_guess(difficulty)
	max_attempts = num_allowed_attempts(difficulty)

	print(num_diff)
	url = "https://www.random.org/integers/?num="+num_diff+"&min=0&max=7&col=1&base=10&format=plain&rnd=new"
	
	# Receive the response and parse it into something usable
	data = requests.get(url, timeout=2.50).text
	print(str(data).replace("\n", ""))

	# Get the date
	now = datetime.now()
	parsed_date = now.strftime("%m/%d/%Y")

	# Define the needed attributes of the CurrentGame
	date = parsed_date
	correct_answer = str(data).replace("\n", "")
	user_email = current_user.email
	status = "In Progress"
	attempt = 0
	new_game = CurrentGame(date=date, correct_answer=correct_answer, user_email = user_email, status=status, attempt=attempt, max_attempts=max_attempts)

	# Add the CurrentGame to the DB
	db.session.add(new_game)
	db.session.commit()

	# Add the current game to the current user
	current_game_id = CurrentGame.query.filter_by(user_email = current_user.email, correct_answer = correct_answer).first().id
	current_user.current_game = current_game_id
	print(current_game_id)
	db.session.commit()

	return render_template('game.html', name=current_user.name, status=new_game.status, difficulty=difficulty, max_attempts=max_attempts, attempt=new_game.attempt)

@main.route('/game', methods=['POST'])
def game_post():
    guess = request.form.get('guess')
    user_email = current_user.email

    current_game = CurrentGame.query.filter_by(id = current_user.current_game).first()

    difficulty = UserPrefs.query.filter_by(user_email = current_user.email).first().difficulty
    
    #Increment number of attempts
    current_game.attempt += 1
    db.session.commit()


    # Game Scoring Logic
    correct_answer = current_game.correct_answer
    attempt = current_game.attempt

    pos = 0
    num = 0
    for i in guess:
    	if i in correct_answer:
    		print("In the string")
    		num +=1
    		if (guess.rfind(i) == correct_answer.rfind(i)):
    			print("In the same position")
    			pos +=1
    
    feedback = ""
    if pos is 0 and num is 0:
    	feedback = "All incorrect"

    else:
    	feedback = str(num) + " correct number and " + str(pos) + " correct positions"

    print(feedback)
    print(current_game.id)

    # Save The Attempt + Feedback
    game_attempt = GameAttempt(parent_game_id=current_game.id, attempt=current_game.attempt, guess=guess, feedback=feedback)
    db.session.add(game_attempt)
    db.session.commit()

    attempts = GameAttempt.query.filter_by(parent_game_id = current_user.current_game)

    if guess == correct_answer:
    	flash('Game Success! You win!')
    	current_game.status = "Won"
    	db.session.commit()

    if guess != correct_answer and current_game.attempt == current_game.max_attempts:
    	flash('Aww, try again next time!')
    	current_game.status = "Lost"
    	db.session.commit()

    return render_template('game.html', name=current_user.name, attempts=attempts, status=current_game.status, correct_answer=current_game.correct_answer, max_attempts= current_game.max_attempts, difficulty=difficulty, attempt=current_game.attempt)

    
    return redirect(url_for('main.game'))

def num_digits_to_guess(level):
	if level == "Hard":
		return "5"
	if level == "Medium":
		return "4"
	if level == "Easy":
		return "3"
	if level == "Zen":
		return "5"

def num_allowed_attempts(level):
	if level == "Zen":
		return 100
	else:
		return 10
