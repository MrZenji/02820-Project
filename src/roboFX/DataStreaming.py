'''
Created on 28/10/2014

@author: Kevin
'''
import json


class DataStreaming(object):
    '''
    This class is responsible for exposing the data
    to the rest of the system, it should be able to
    use both live data as well as history data.
    '''

    def __init__(self, filename="data.txt"):
        '''
        Load the data from a file
        '''
        jFile = open(filename)
        self.data = json.load(jFile)
        jFile.close()
        self.count = 0
        self.maxCount = len(self.data['candles'])

    def getData(self):
        self.count += 1
        return self.data['candles'][self.count-1]

    def reload(self):
        self.count = 0
