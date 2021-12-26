from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_from_directory
import os
import sys

from plausiblewords import WordPlausibilityEvaluator
from dailyletters import DailyLetters

app = Flask(__name__)

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
    return dl.getDailyLetters()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

def is_pangram(word):
    for letter in dl.getDailyLetters():
        if letter not in word:
            return False
    return True

def valid_letters(word):
    letters = dl.getDailyLetters()
    if letters[0] not in word:
        print(letters[0], "not in word", word)
        return False
    for letter in word:
        if letter not in letters:
            print(letter, "not in letters", letters)
            return False
    return True

if __name__ == '__main__':
    evaluator = WordPlausibilityEvaluator()
    evaluator.populate_dict('words_alpha.txt')
    dl = DailyLetters()
    print('Starting server with letters: {}'.format(dl.getDailyLetters()))

    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        app.run(port=8998, debug=True);
    else:
        app.run(port=8998, debug=False);

