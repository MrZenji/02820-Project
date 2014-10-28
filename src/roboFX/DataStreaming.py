'''
Created on 28/10/2014

@author: Kevin
'''


class DataStreaming(object):
    '''
    This class is responsible for exposing the data
    to the rest of the system, it should be able to
    use both live data as well as history data.
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.instrument = "EUR_USD"

    def getData(self):
        print "5-min worth of data"