from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import send_from_directory
import os
import sys
import logging
import atexit

from plausiblewords import WordPlausibilityEvaluator
from rnn_plausiblewords import RnnWordPlausibilityEvaluator
from dailyletters import DailyLetters
from records import Records

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html', totalPlausibleWords=totalPlausibleWords,
            displayDate = dl.getDisplayDate())

@app.route('/try/<word>', methods=['POST'])
def check_word(word):
    global totalPlausibleWords, totalAttempts

    totalAttempts += 1
    if not valid_letters(word):
        return 'wrong'
    starword = '*' + word.lower() + '*'
    if evaluator.is_word(starword):
        return 'real'
    elif rnn_evaluator.is_plausible(word):
        totalPlausibleWords += 1

        if is_pangram(word):
            return 'pangram'
        else:
            return 'good'
    else:
        return 'bad'

@app.route('/letters', methods=['GET'])
def get_letters():
    return dl.getDailyLetters().lower()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
            'favicon.ico', mimetype='image/vnd.microsoft.icon')

def is_pangram(word):
    for letter in get_letters():
        if letter not in word:
            return False
    return True

def valid_letters(word):
    letters = get_letters()
    if letters[0] not in word:
        return False
    for letter in word:
        if letter not in letters:
            return False
    return True

def save_records_on_exit():
    global totalPlausibleWords, totalAttempts
    records.saveRecord(Records.TOTAL_PLAUSIBLE, totalPlausibleWords)
    records.saveRecord(Records.TOTAL_ATTEMPTS, totalAttempts)
    atexit.unregister(save_records_on_exit)
    app.logger.info('Records saved on exit.')


def init_record(initialVal, recordName):
    try:
        return records.loadRecord(recordName)
    except FileNotFoundError:
        records.saveRecord(Records.TOTAL_PLAUSIBLE, initialVal)
        return initialVal

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    evaluator = WordPlausibilityEvaluator(app.logger)
    evaluator.populate_dict('words_alpha.txt')
    rnn_evaluator = RnnWordPlausibilityEvaluator(app.logger)

    dl = DailyLetters(app.logger)

    records = Records(app.logger)
    global totalPlausibleWords, totalAttempts
    totalPlausibleWords = init_record(0, Records.TOTAL_PLAUSIBLE);
    totalAttempts = init_record(0, Records.TOTAL_ATTEMPTS)
    atexit.register(save_records_on_exit)

    app.logger.info('Starting Spolling Bree server with letters: {}'.format(get_letters()))

    if len(sys.argv) >= 2 and sys.argv[1] == "debug":
        # when using reloader the atexit hook runs twice and overwrites itself
        app.run(port=8998, debug=True, use_reloader=False);
    else:
        # automatically no reloader if debug=False
        app.run(port=8998, debug=False);

