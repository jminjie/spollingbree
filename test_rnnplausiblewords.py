from rnn_plausiblewords import RnnWordPlausibilityEvaluator
import logging

rnn_evaluator = RnnWordPlausibilityEvaluator(logging, temperature=1)

def print_and_eval(word, show_work=False):
    print('score for *{0}*: {1} - {2}'.format(word,
        rnn_evaluator.evaluate_word(word, show_work),
        'plausible' if rnn_evaluator.is_plausible(word) else 'no'))

print_and_eval('atata')
print_and_eval('atatata')
print_and_eval('atatatata')
print_and_eval('atatatatata')
print_and_eval('atatatatatata')
print_and_eval('atatatatatatata')

print_and_eval('multinnn', True)
print_and_eval('tiontiontion', True)
