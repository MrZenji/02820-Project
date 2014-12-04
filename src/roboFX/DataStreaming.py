'''
Created on 28/10/2014

@author: Kevin
'''
import json


class DataStreaming(object):
    '''
    This class is responsible for exposing the data
    to the rest of the system, it is only using
    historical data from a file.
    '''

    def __init__(self, filename="data.txt"):
        '''
        Load the data from a file
        '''
        jFile = open(filename)
        self.data = json.load(jFile)
        jFile.close()
        self.count = 0
        self.maxCount = len(self.data)

    def getData(self):
        '''Returns a candle of data'''
        self.count += 1
        return self.data[self.count-1]

    def reload(self):
        '''Reset data the pointer'''
        self.count = 0
