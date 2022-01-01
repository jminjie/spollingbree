import math

# Used to evaulate the plausibilitiy of a word based on its spelling
class WordPlausibilityEvaluator:
    def __init__(self, logger):
        self.trigram_dictionary = {}
        # penalty for long words
        self.lamda = 3.5
        self.cap = 0.6
        self.all_words = set()
        self.logger = logger

        # unused
        self.AVERAGE_TRIGRAM_COUNT = 350
        self.BAD_TRIGRAM_PENALTY = 1000000

    def add_to_dict(self, word):
        if word[0] != '*' or word[-1] != '*':
            print('Word must begin and end with * character')
            return;
        numChars = len(word)
        self.all_words.add(word)
        i = 0;
        while i <= numChars - 3:
            trigram = word[i:i+3]
            if trigram in self.trigram_dictionary.keys():
                self.trigram_dictionary[trigram] += 1
            else:
                self.trigram_dictionary[trigram] = 1
            i += 1

    def populate_dict(self, filename):
        with open(filename, "r") as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                line = '*' + line.strip('\n ') + '*'
                # min of 4 letter word plus two word boundaries
                if len(line) >= 6:
                    self.add_to_dict(line)
        self.normalize()

    def normalize(self):
        maxCount = 0
        for key in self.trigram_dictionary.keys():
            if self.trigram_dictionary[key] > maxCount:
                maxCount = self.trigram_dictionary[key]

        # scale to between 0-1, then cap to max value
        for key in self.trigram_dictionary.keys():
            self.trigram_dictionary[key] = min(self.cap, (self.trigram_dictionary[key] / maxCount))

    def eval_word(self, word):
        if word[0] != '*' or word[-1] != '*':
            print('Word must begin and end with * character')
            return;
        numChars = len(word)
        i = 0;
        score = 0
        while i <= numChars - 3:
            trigram = word[i:i+3]
            if trigram in self.trigram_dictionary.keys():
                score += self.trigram_dictionary[trigram]
            else:
                return -100
            i += 1
        return score / (self.lamda * pow(max(numChars - 5, 1), 1.7))

    def is_plausible(self, word):
        if word[0] != '*' or word[-1] != '*':
            print('Word must begin and end with * character')
            return
        # TODO: use the average score of the possible words given the letters
        return self.eval_word(word) > 0.02

    def is_word(self, word):
        if word[0] != '*' or word[-1] != '*':
            print('Word must begin and end with * character')
            return
        return word in self.all_words

    # this is around 60 for the 20k most common words
    def get_average_score(self, filename):
        with open(filename, "r") as fp:
            averageScore = 0;
            numWords = 0
            while True:
                line = fp.readline()
                if not line:
                    break
                line = '*' + line.strip('\n ') + '*'
                # min of 4 letter word plus two word boundaries
                if (len(line) >= 6):
                    averageScore += self.eval_word(line)
                    numWords += 1
            return averageScore / numWords

    def get_average_trigram_count(self):
        averageCount = 0
        for pair in self.trigram_dictionary.values():
            averageCount += pair
        return averageCount / len(self.trigram_dictionary)
