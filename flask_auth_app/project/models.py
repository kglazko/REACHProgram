from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class GameResults(db.Model):
	id = db.Column(db.Integer, primary_key=True)# primary keys are required by SQLAlchemy
	date = db.Column(db.String(100))
	user_email = db.Column(db.String(100))
	attempts = db.Column(db.String(100))
	outcome = db.Column(db.String(1000))

class CurrentGame(db.Model):
	id = db.Column(db.Integer, primary_key=True)# primary keys are required by SQLAlchemy
	correct_answer = db.Column(db.String(100))
	status = db.Column(db.String(100))
	attempt = db.Column(db.Integer)