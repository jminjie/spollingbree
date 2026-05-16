from datetime import datetime, timezone
from datetime import date
import pytz
import os
import calendar
import urllib.request
import re
import requests

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
        return '{:0>2d}/{:0>2d}/{:0>2d}'.format(now.year, now.month, now.day)

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
        # This is a Spelling Bee clone with a less restrictive scraping policy
        url = 'https://www.sbsolver.com/answers'
        self.logger.warning('Attempting download from {}'.format(url))

        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)

        # TODO saves it to /tmp
        filename, _ = urllib.request.urlretrieve(url)

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
        MARKER = 'alt="center letter'
        # sbsolver includes a line with the daily letters which looks like
        #
        # alt="center letter M" /><a href="https://www.sbsolver.com/s/mAcginp"
        markedString = ''
        with open(filename, 'r') as fopen:
            for line in fopen:
                if MARKER in line:
                    index = line.find(MARKER);
                    markedString = line[index:index+100]
                    break
        print(markedString)
        letters = markedString[60:67]

        url = "https://www.reddit.com/r/NYTSpellingBee/.json"
        headers = {"User-Agent": "spelling-bee-scraper/1.0"}

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        posts = response.json()["data"]["children"]
        for post in posts:
            title = post["data"]["title"]
            if date_str in title:
                match = re.search(r'\(([A-Za-z])\)\s*([A-Za-z\s]+)', title)
                if match:
                    center = match.group(1)
                    others = match.group(2).split()
                    letters = "".join([center] + others).lower()
                    # save to cache and file
                    self.__cachedLetters = letters
                    self.__saveCachedLetters(letters)
                    with open(self.DATE_FILE, 'w') as f:
                        f.write(self.getDate());
                    return letters


        raise ValueError(f"No Reddit post found for {date_str}")

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

        return self.__getLettersFromReddit()
