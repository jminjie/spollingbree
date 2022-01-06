from plausiblewords import WordPlausibilityEvaluator
import logging

evaluator = WordPlausibilityEvaluator(logging)
evaluator.populate_dict('words_alpha.txt')

def print_implausible_word(num=100):
    with open('words_alpha.txt', "r") as fp:
        for i in range(0, num):
            line = fp.readline()
            if not line:
                break
            line = '*' + line.strip('\n ') + '*'
            # min of 4 letter word plus two word boundaries
            if len(line) >= 6:
                if not evaluator.is_plausible(line):
                    print(line, evaluator.eval_word(line))

print('average score of alpha', evaluator.get_average_score('words_alpha.txt'))
print('average score of 20k', evaluator.get_average_score('20k.txt'))

def print_and_eval(word):
    word_with_boundaries = '*' + word + '*'
    print('score for *{0}*: {1} - {2}'.format(word,
        evaluator.eval_word(word_with_boundaries),
        'plausible' if evaluator.is_plausible(word_with_boundaries) else 'no'))

print_implausible_word(50)

print_and_eval("axax")
print_and_eval("butt")
print_and_eval("jokging")
print_and_eval("jonging")
print_and_eval("brog")
print_and_eval("stillington")
print_and_eval("clogged")
print_and_eval("atata")
print_and_eval("atatata")
print_and_eval("atatatatat")
print_and_eval("atatatatatat")
print_and_eval("lyly")
print_and_eval("royall")
print_and_eval("layor")
print_and_eval("tryng")
print_and_eval("riyng")
print_and_eval("crommy")

assert(evaluator.is_plausible('*jonging*'))
assert(not evaluator.is_plausible('*atatata*'))
assert(not evaluator.is_plausible('*atatatata*'))
assert(not evaluator.is_plausible('*atatatatata*'))

assert(evaluator.is_word('*stupid*'))
assert(evaluator.is_word('*jogging*'))
assert(not evaluator.is_word('*jonging*'))
assert(not evaluator.is_word('*slkdfj*'))

print('------------ALL TESTS PASSED------------')
