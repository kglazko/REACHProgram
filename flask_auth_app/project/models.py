from flask_login import UserMixin
from . import db

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

class GameAttempt(db.Model):
	id = db.Column(db.Integer, primary_key=True)# primary keys are required by SQLAlchemy
	parent_game_id = db.Column(db.String(100))
	attempt = db.Column(db.Integer)
	guess = db.Column(db.String(100))
	feedback = db.Column(db.String(100))