from datetime import datetime, timezone
import wget
import pytz
import os
import calendar

class DailyLetters:
    def __init__(self, logger):
        self.__lastDownloadedFileName = ''
        self.__cachedLetters = ''
        self.logger = logger

        # dir for temp files
        self.TEMP_DIR = 'temp'

        # dir for cached letters
        self.CACHED_LETTERS_FILE = 'temp/letters.txt'

        # temp file which contains the date we last downloaded the letters
        self.DATE_FILE = 'temp/date.txt'

        # temp file which contains the name of the last downloaded NYT forum html file
        self.LAST_DOWNLOADED_FILE = 'temp/lastdownloaded.txt'

    def getDate(self):
        # the NYTSB Forum post is usually posted around 3 am ET (12 am PT)
        # so to be safe we use date from Hawaii time (2 hours behind PT)
        # this means that our letters won't update until 2 am PT but this should be fine
        timezone = pytz.timezone('US/Hawaii')
        now = datetime.now(timezone)
        return '{0}/{1}/{2}'.format(now.year, now.month, now.day)

    def getDisplayDate(self):
        timezone = pytz.timezone('US/Hawaii')
        now = datetime.now(timezone)
        return '{0} {1}, {2}'.format(calendar.month_name[now.month], now.day, now.year)

    def __downloadFileIfNeeded(self):
        date = self.getDate()
        if self.__alreadyDownloadedToday(date):
            if self.__lastDownloadedFileName != '':
                return self.__lastDownloadedFileName
            else:
                try:
                    self.__lastDownloadedFileName = self.__loadLastDownloadedFileName()
                    return self.__lastDownloadedFileName
                except FileNotFoundError:
                    self.logger.error('Expected to find cached filename but could not.');

        if not os.path.exists(self.TEMP_DIR):
                os.makedirs(self.TEMP_DIR)
        self.logger.warning('Disk cache miss in getDailyLetters, downloading.')
        url = 'https://www.nytimes.com/{}/crosswords/spelling-bee-forum.html'.format(date)
        filename = wget.download(url, out=self.TEMP_DIR)
        with open(self.DATE_FILE, 'w') as f:
            f.write(date);

        self.__saveLastDownloadedFileName(filename)
        return filename

    def __loadLastDownloadedFileName(self):
        with open(self.LAST_DOWNLOADED_FILE, 'r') as f:
            return f.read()

    def __saveLastDownloadedFileName(self, filename):
        with open(self.LAST_DOWNLOADED_FILE, 'w') as f:
            return f.write(filename)

    def __loadCachedLetters(self):
        with open(self.CACHED_LETTERS_FILE, 'r') as f:
            return f.read()

    def __saveCachedLetters(self, letters):
        with open(self.CACHED_LETTERS_FILE, 'w') as f:
            return f.write(letters)


    def __alreadyDownloadedToday(self, date):
        try:
            with open(self.DATE_FILE, 'r') as f:
                if f.read() == date:
                    return True
                else:
                    return False
        except FileNotFoundError:
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
        if self.__alreadyDownloadedToday(self.getDate()):
            if (self.__cachedLetters != ''):
                return self.__cachedLetters
            else:
                self.logger.warning('Memory cache miss in getDailyLetters')
                try:
                    self.__cachedLetters = self.__loadCachedLetters()
                    return self.__cachedLetters
                except FileNotFoundError:
                    self.logger.error('Expected to find cached letters but could not.');

        return self.__getLettersFromFile(self.__downloadFileIfNeeded())
