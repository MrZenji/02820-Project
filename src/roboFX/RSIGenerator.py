'''
Created on 28/10/2014
@author: s103451
'''
import talib
import numpy as np


class RSIGenerator(object):
    '''
    This class performs the analasys of the data
    '''

    def __init__(self):
        '''
        All of the OCHL data uses the bid prices
        '''
        self.open = [None] * 100
        self.close = [None]*100
        self.high = [None]*100
        self.low = [None]*100
        self.volume = [None]*100

    def analyse(self, data):
        self.open.pop(0)
        self.open.append(data['openBid'])
        self.close.pop(0)
        self.close.append(data['closeBid'])
        self.high.pop(0)
        self.high.append(data['highBid'])
        self.low.pop(0)
        self.low.append(data['lowBid'])
        self.volume.pop(0)
        self.volume.append(data['volume'])

        if None not in self.open:
            rsi = talib.RSI(np.array(self.close))[-1]
            if rsi > 70:
                return 1
            elif rsi < 30:
                return -1
            else:
                return 0
        else:
            return 0
