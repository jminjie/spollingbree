from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_from_directory
import os
import sys

from words import WordPlausibilityEvaluator
from dailyletters import getDailyLetters

app = Flask(__name__)

LETTERS = getDailyLetters().lower()

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/try/<word>', methods=['POST'])
def check_word(word):
    if not valid_letters(word):
        return 'wrong'

    word = '*' + word.lower() + '*'
    if evaluator.is_word(word):
        return 'real'
    elif evaluator.is_plausible(word):
        if is_pangram(word):
            return 'pangram'
        else:
            return 'good'
    else:
        return 'bad'

@app.route('/letters', methods=['GET'])
def get_letters():
    return LETTERS

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

def is_pangram(word):
    for letter in LETTERS:
        if letter not in word:
            return False
    return True

def valid_letters(word):
    if LETTERS[0] not in word:
        print(LETTERS[0], "not in word", word)
        return False
    for letter in word:
        if letter not in LETTERS:
            print(letter, "not in LETTERS", LETTERS)
            return False
    return True

evaluator = WordPlausibilityEvaluator()
evaluator.populate_dict('words_alpha.txt')

if len(sys.argv) >= 2 and sys.argv[1] == "debug":
    app.run(port=8998, debug=True);
else:
    app.run(port=8998, debug=False);

