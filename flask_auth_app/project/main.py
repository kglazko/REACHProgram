import requests
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
	# Send a request to the random int API
	url = "https://www.random.org/integers/?num=4&min=0&max=7&col=1&base=10&format=plain&rnd=new"
	
	# Receive the response and parse it into something usable
	data = requests.get(url, timeout=2.50).text
	print(str(data).replace("\n", ""))

	# Define the needed attributes of the CurrentGame
	correct_answer = str(data).replace("\n", "")
	user_email = current_user.email
	status = "not won"
	attempt = 0
	new_game = CurrentGame(correct_answer=correct_answer, user_email = user_email, status=status, attempt=attempt)

	# Add the CurrentGame to the DB
	db.session.add(new_game)
	db.session.commit()

	# Add the current game to the current user
	current_game_id = CurrentGame.query.filter_by(user_email = current_user.email, correct_answer = correct_answer).first().id
	current_user.current_game = current_game_id
	print(current_game_id)
	db.session.commit()

	return render_template('game.html', name=current_user.name)

@main.route('/game', methods=['POST'])
def game_post():
    guess = request.form.get('guess')
    user_email = current_user.email

    current_game = CurrentGame.query.filter_by(id = current_user.current_game).first()
    
    #Increment number of attempts
    current_game.attempt += 1
    db.session.commit()

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

    if attempt == 1:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_1 = feedback)

    elif attempt == 2:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_2 = feedback)

    elif attempt == 3:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_3 = feedback)

    elif attempt == 4:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_4 = feedback)

    elif attempt == 5:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_5 = feedback)

    elif attempt == 6:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_6 = feedback)

    elif attempt == 7:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_7 = feedback)

    elif attempt == 8:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_8 = feedback)

    elif attempt == 9:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_9 = feedback)

    else:
    	return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback_10 = feedback)


    
    if guess == "1234":
        return render_template('game.html', name=current_user.name, attempt= str(current_game.attempt), feedback = feedback)
    
    return redirect(url_for('main.game'))
