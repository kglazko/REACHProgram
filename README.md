# REACHProgram
## Introduction
I decided to implement my Mastermind game using Python, on a web interface. I used Flask as the web framework. My goals for this challenge were:
* Set up the basics of the Mastermind game outlined in the instructions in simple Python, integrating the random num API call
* Create a Flask web app where people can login, play the game, and see their past game scores
* Create difficulty levels in the Flask web app that change the nature of the game
* Do this in a "back-end" way... that's right, I have Flask auth, databases, and templates that update based on the databases. This is definitely not my typical wheelhouse, see https://kglazko.github.io for my typical style of web dev.

## Game Details
### Original Game Instructions
* At the start of the game the computer will randomly select a pattern of four different
numbers from a total of 8 different numbers.
* A player will have 10 attempts to guess the number combinations
* At the end of each guess, computer will provide one of the following response as
feedback:
  * The player had guess a correct number
  * The player had guessed a correct number and its correct location
  * The player’s guess was incorrect

```Example Run:
Game initializes and selects “0 1 3 5”
Player guesses “2 2 4 6”, game responds “all incorrect”
Player guesses “0 2 4 6”, game responds “1 correct number and 1 correct location”
Player guesses “2 2 1 1”, game responds “1 correct number and 0 correct location”
Player guesses “0 1 5 6”, game responds “3 correct numbers and 2 correct location”
...
```
Note that the computer’s feedback should not reveal which number the player guessed
correctly

### Updated Game Instructions
* Game Difficulty is a new feature of the game. Game difficulty changes the quantity of numbers in the pattern. All levels except Zen Mode will give you 10 attempts.
  * _Easy_ gives you a pattern of 3 numbers.
  * _Medium_ gives you a pattern of 4 numbers.
  * _Hard_ gives you a pattern of 5 numbers.
  * _Zen_ gives you a pattern of 5 numbers, and 100 attempts to figure out the puzzle.
 
 ## How to Run
 ### On your local computer
 * Clone or download the repository
 * Install the dependencies in the requirements.txt in your choice of virtual or non-virtual environment.
 * Run the following commands: `export FLASK_APP=project` and `export FLASK_DEBUG=1`
 * Once you do this, you can run the application from the flask_app_auth folder using `flask run`
 
 ### On DigitalOcean
 * As of tonight, they are having service issues relating to project URLs: https://status.digitalocean.com/incidents/y02k6rjpz6tm
 * I got my project deployed finally (gunicorn is complicated) and then the URL wouldn't work. Hopefully it will tomorrow, https://whale-app-gmx7a.ondigitalocean.app/

## Development Process
### Flask app and authentication
* The Flask login/sign-up was based on the tutorial from https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
* The `game.html` and `game_menu.html` templates were added- this is where the gameplay happens once a user is logged in. The `profile.html` page now has the important task of containing a user's game scores.
* The game logic- and the updates to the `game`, `game_menu`, and `profile` templates as the game is played- lives within `main.py`. Login/sign-up related work lives within `auth.py`.

### Databases
* I tried to minimize hard-coding. As a result, I added to the auth tutorial's `model.py` to create a tables for user preferences, a game object, and guess attempts.
```
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    current_game = db.Column(db.Integer)

class UserPrefs(db.Model):
	id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
	user_email = db.Column(db.String(100), unique=True)
	difficulty = db.Column(db.String(100))

class CurrentGame(db.Model):
	id = db.Column(db.Integer, primary_key=True)# primary keys are required by SQLAlchemy
	date = db.Column(db.String(100))
	correct_answer = db.Column(db.String(100))
	user_email = db.Column(db.String(100))
	status = db.Column(db.String(100))
	attempt = db.Column(db.Integer)
	max_attempts = db.Column(db.Integer)

class GameAttempt(db.Model):
	id = db.Column(db.Integer, primary_key=True)# primary keys are required by SQLAlchemy
	parent_game_id = db.Column(db.String(100))
	attempt = db.Column(db.Integer)
	guess = db.Column(db.String(100))
	feedback = db.Column(db.String(100))
```
* `UserPrefs` currently tracks the game difficulty a user has selected when starting the game. `CurrentGame`, named a bit poorly perhaps, represents a game that is or was played by a player. It tracks important game features like the correct answer, the number of guesses a user has made, and the max number of attempts (10 except in Zen Mode).`GameAttempt` tracks the guesses themselves a user has made for a specific game, as well as feedback strings that accompany those guesses. The primary purpose of this table was just to display the attempts and feedback to the user in a way that persists despite the template re-rendering with each guess.
* Flask has a nice `current_user` feature that makes it very easy to identify the user, so most of the tables hinge on the current user and the `current_game` that is updated as they start a new game. The game ID represented by `current_game` is important to all the updates happening due to the game logic.

### Game Logic
* The random number generation occurs in `main.py`, namely: 
```
url = "https://www.random.org/integers/?num="+num_diff+"&min=0&max=7&col=1&base=10&format=plain&rnd=new"
data = requests.get(url, timeout=2.50).text
correct_answer = str(data).replace("\n", "")
```
* `num_diff` is determined by the difficult level, and a simple if-based function determines that.
* The user then types guesses into the form seen in the `game.html` template. Every time they submit a guess, the response is checked against the correct answer. Attempt numbers are incremented, and when a user reaches the attempt limit, the game will end and they will be prompted to try again or see their results on their profile through a `flash`. Likewise, if the user succeeds, they will be congratulated and offered the same options (once again, this takes place in `main.py`.
* The game logic to determine whether a number or position is correct is the following:
```
def calculate_correct_numbers(guess, answer):
	num = 0
	guess_set = set(guess)

	for i in guess_set:
		guess_instances = guess.count(i)
		answer_instances = answer.count(i)
		if answer_instances > 0:
			if guess_instances > answer_instances:
				num += answer_instances

			else:
				num += guess_instances
	return num

def calculate_correct_position(guess,answer):
	pos = 0
	for i in range (0, len(guess)):
		if guess[i] == answer[i]:
			pos +=1
	return pos
```
### Flask-Driven UI Updates
* During both selecting a game mode and game play, when a player submits a combination, it results in a `POST` which is then addressed through the appropriate method, all of which are in `main.py`.
* The code in the template `game_menu.html` shows the following in the form where the POST happens:
```
<form form method="POST" action="/game_menu">
  <div class="field">
                <div class="control">
            <h2 id="scores">
  Select a Mode
</h2>
            <div class="select is-primary">
              <select name="difficulty">
              <option>Zen</option>
              <option>Easy</option>
              <option>Medium</option>
              <option>Hard</option>
              </select>
            </div>

            <button class="button is-success">Start Game</button>
          </div>
        </div>
        </form>
```
* Meanwhile, in `main.py`, this is what happens when a POST happens, relating to `game_menu`:
```
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
```
* Similarly, `game` has complex interactions that happen when an attempted guess `POST`. Notably, we re-render the `game` template with the updated game state, number of guesses, feedback from previous attempts, and the correct answer (for when the game is over).
```
return render_template('game.html', name=current_user.name, attempts=attempts, status=current_game.status, correct_answer=current_game.correct_answer, max_attempts= current_game.max_attempts, difficulty=difficulty, attempt=current_game.attempt)
```
## Features
### Cool additions and extras!
* The sign-up, login, and profile page that tracks your scores.
* We already detailed the difficulty selection, but yes, that is a thing. I was proud of my work putting it as a user pref in a database table, and changing the URL request based on the difficulty. Additionally, I modify the text within the typing box for the guesses based on the difficulty level, prompting users to type 3, 4, or 5 characters depending on the difficulty.
* I have some cool game-end logic, powered by `flash` in `flask`. I am able to display messages in game-over instances. It adds a nice, UI touch. I am also reveal the correct answer to folks at the end, again, powered by templating and the DB.
* DigitalOcean deployment, although only time will tell if it worked.

### To-Dos
* It would be nice to have some form of limiting how many numbers a user can type based on the difficulty level, and limiting them to only inputting characters between 0-7 (you can do all of them now).
* Ability to sort results on the profile page.

## My Reflections
* I am kind of amazed by the fact I was actually able to take the theory from my CS DB class and make optimized database tables in real life (I know, with some redundancy for convenience), and integrate them into my app to make it so much less hard-coded than I usually would. I have never done this before on my own.
* I am very proud of all of the code that I wrote in `main.py`. It is very far outside of my normal coding domain. 
* Deploying to DigitalOcean was difficult and confusing, but if I get a live-running game out of it, it will be worth it.
