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
                    print(line)

print('average score of alpha', evaluator.get_average_score('words_alpha.txt'))
print('average score of 20k', evaluator.get_average_score('20k.txt'))

print('score for *axax*', evaluator.eval_word('*axax*'))
print('score for *butt*', evaluator.eval_word('*burt*'))
print('score for *jokging*', evaluator.eval_word('*jokging*'))
print('score for *jonging*', evaluator.eval_word('*jonging*'))
print('score for *brog*', evaluator.eval_word('*brog*'))
print('score for *stillington*', evaluator.eval_word('*stillington*'))
print('score for *clogged*', evaluator.eval_word('*clogged*'))
print('score for *atata*', evaluator.eval_word('*atata*'))
print('score for *atatata*', evaluator.eval_word('*atatata*'))
print('score for *atatatatat*', evaluator.eval_word('*atatatatat*'))
print('score for *atatatatatat*', evaluator.eval_word('*atatatatatat*'))
print('score for *lyly*', evaluator.eval_word('*lyly*'))
print('score for *royall*', evaluator.eval_word('*royall*'))
print('score for *layor*', evaluator.eval_word('*layor*'))

print('*axax*', evaluator.is_plausible('*axax*'))
print('*butt*', evaluator.is_plausible('*burt*'))
print('*jokging*', evaluator.is_plausible('*jokging*'))
print('*jonging*', evaluator.is_plausible('*jonging*'))
print('*brog*', evaluator.is_plausible('*brog*'))
print('*stillington*', evaluator.is_plausible('*stillington*'))
print('*clogged*', evaluator.is_plausible('*clogged*'))
print('*atata*', evaluator.is_plausible('*atata*'))
print('*atatata*', evaluator.is_plausible('*atatata*'))
print('*atatatatat*', evaluator.is_plausible('*atatatatat*'))
print('*atatatatatat*', evaluator.is_plausible('*atatatatatat*'))
print('*lyly*', evaluator.is_plausible('*lyly*'))

assert(evaluator.is_plausible('*jonging*'))
assert(evaluator.is_plausible('*clogged*'))
assert(not evaluator.is_plausible('*atatata*'))
assert(not evaluator.is_plausible('*atatatata*'))
assert(not evaluator.is_plausible('*atatatatata*'))


assert(evaluator.is_word('*stupid*'))
assert(evaluator.is_word('*jogging*'))
assert(not evaluator.is_word('*jonging*'))
assert(not evaluator.is_word('*slkdfj*'))

print('------------ALL TESTS PASSED------------')
