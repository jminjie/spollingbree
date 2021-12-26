import os

class Records:
    TOTAL_ATTEMPTS = 'totalattempts.txt'

    def __init__(self, logger):
        self.__RECORDS_DIR = 'records/'
        self.__logger = logger
        if not os.path.exists(self.__RECORDS_DIR):
            os.makedirs(self.__RECORDS_DIR)


    def saveRecord(self, recordName, value):
        with open(self.__RECORDS_DIR + recordName, 'w') as f:
            f.write(str(value))
            self.__logger.info('Wrote value {0} to recordName {1}'.format(value, recordName))

    def loadRecord(self, recordName):
        with open(self.__RECORDS_DIR + recordName, 'r') as f:
            value = int(f.read())
            self.__logger.info('Read value {0} from recordName {1}'.format(value, recordName))
            return value

