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

    def __getLettersFromReddit(self):
        today = date.today()
        date_str = today.strftime("%B %-d, %Y")  # e.g. "May 15, 2026"

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
