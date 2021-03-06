from rnn_plausiblewords import RnnWordPlausibilityEvaluator
import logging

rnn_evaluator = RnnWordPlausibilityEvaluator(logging, temperature=1)

def print_and_eval(word, show_work=False):
    print('score for *{0}*: {1} - {2}'.format(word,
        rnn_evaluator.evaluate_word(word, show_work),
        'plausible' if rnn_evaluator.is_plausible(word) else 'no'))

print_and_eval('at', True)

print_and_eval('atatata')
print_and_eval('atatatata')
print_and_eval('atatatatata')
print_and_eval('atatatatatata')
print_and_eval('atatatatatatata')
print_and_eval('multinnn')
print_and_eval('tiontiontion')

print_and_eval('sloggery', True)
print_and_eval('yondry', True)
print_and_eval('clarking', True)

print_and_eval('cron')
print_and_eval('slam')
print_and_eval('spit')

print_and_eval('brun')
print_and_eval('gluk')
print_and_eval('lyly')
print_and_eval('pithc')
print_and_eval('pitchc')
print_and_eval('chtcht', True)
