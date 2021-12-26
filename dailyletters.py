import wget
from datetime import datetime

class DailyLetters:
    def __init__(self):
        self.__lastDownloadedFileName = ''
        self.__cachedLetters = ''

        # dir for cached letters
        self.CACHED_LETTERS_FILE = 'temp/letters.txt'

        # temp file which contains the date we last downloaded the letters
        self.DATE_FILE = 'temp/date.txt'

        # temp file which contains the name of the last downloaded NYT forum html file
        self.LAST_DWONLOADED_FILE = 'temp/lastdownloaded.txt'

    def __getDate(self):
        now = datetime.now()
        return '{0}/{1}/{2}'.format(now.year, now.month, now.day)

    def __downloadFileIfNeeded(self):
        date = self.__getDate()
        if self.__alreadyDownloadedToday(date):
            if self.__lastDownloadedFileName != '':
                return self.__lastDownloadedFileName
            else:
                try:
                    self.__lastDownloadedFileName = self.__loadLastDownloadedFileName()
                    return self.__lastDownloadedFileName
                except FileNotFoundError:
                    print('Expected to find cached filename but could not. Doing download.');

        url = 'https://www.nytimes.com/{}/crosswords/spelling-bee-forum.html'.format(date)
        filename = wget.download(url, out='temp/')
        with open(self.DATE_FILE, 'w') as f:
            f.write(date);

        self.__saveLastDownloadedFileName(filename)
        return filename

    def __loadLastDownloadedFileName(self):
        with open(self.LAST_DWONLOADED_FILE, 'r') as f:
            return f.read()

    def __saveLastDownloadedFileName(self, filename):
        with open(self.LAST_DWONLOADED_FILE, 'w') as f:
            return f.write(filename)

    def __loadCachedLetters(self):
        with open(self.CACHED_LETTERS_FILE, 'r') as f:
            return f.read()

    def __saveCachedLetters(self, letters):
        with open(self.CACHED_LETTERS_FILE, 'w') as f:
            return f.write(letters)


    def __alreadyDownloadedToday(self, date):
        with open(self.DATE_FILE, 'r') as f:
            if f.read() == date:
                return True
            else:
                return False

    def __getLettersFromFile(self, filename):
        MARKER = 'Center letter is in'
        markedString = ''
        with open(filename, 'r') as fopen:
            for line in fopen:
                if MARKER in line:
                    index = line.find(MARKER);
                    markedString = line[index:index+200]
                    break
        # subString is of the form 'Y</strong> A B D L O'
        subString = markedString[141:163]

        letters = subString[0] + subString[11] + subString[13] + subString[15] + \
                subString[17] + subString[19] + subString[21]

        # save to cache and file
        self.__cachedLetters = letters
        self.__saveCachedLetters(letters)
        return letters

    def getDailyLetters(self):
        if self.__alreadyDownloadedToday(self.__getDate()):
            if (self.__cachedLetters != ''):
                print('Cache hit')
                return self.__cachedLetters
            else:
                print('Cache miss')
                try:
                    self.__cachedLetters = self.__loadCachedLetters()
                    return self.__cachedLetters
                except FileNotFoundError:
                    print('Expected to find cached letters but could not. Doing download.');

        return self.__getLettersFromFile(self.__downloadFileIfNeeded())
