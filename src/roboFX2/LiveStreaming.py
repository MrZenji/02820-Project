'''
Created on 28/10/2014

@author: Kevin
'''
from oandapy import oandapy


class LiveStreaming(object):
    '''
    This class is responsible for exposing the data
    to the rest of the system, it should be able to
    use both live data as well as history data.
    '''

    def __init__(self, granularity="M5", instrument="EUR_USD"):
        '''
        Load the data from a oanda
        '''
        self.oanda = oandapy.API(environment="practice",
                                 access_token="e53fd8cfdb5f5e58c15f0936ece50939-4431fd4def9be7d92abb7ede43738eb4")
        self.instrument = instrument
        self.granularity = granularity

    def getData(self):
        liveData = self.oanda.get_history(instrument=self.instrument, count=1,
                                          granularity=self.granularity)
        return liveData["candles"][0]
