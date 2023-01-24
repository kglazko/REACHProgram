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


