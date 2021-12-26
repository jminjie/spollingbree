import wget
from datetime import datetime

def getDate():
    now = datetime.now()
    return '{0}/{1}/{2}'.format(now.year, now.month, now.day)

def downloadFile():
    date = getDate()
    url = 'https://www.nytimes.com/' + date + '/crosswords/spelling-bee-forum.html'
    filename = wget.download(url)
    return filename

def getLettersFromFile(filename):
    MARKER = 'Center letter is in'
    markedString = ''
    with open(filename, 'r') as fopen:
        for line in fopen:
            if MARKER in line:
                index = line.find(MARKER);
                markedString = line[index:index+200]
                break
    # subString is of the form
    # Y</strong> A B D L O 
    subString = markedString[141:163]

    letters = subString[0] + subString[11] + subString[13] + subString[15] + \
            subString[17] + subString[19] + subString[21]
    print(letters)
    return letters

def getDailyLetters():
    return getLettersFromFile(downloadFile())
