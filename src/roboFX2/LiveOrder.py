'''
Created on 28/10/2014
@param instrument: The currency pair being traded
@param units: The amount of valuta you would like to trade
@author: s103451
'''
from roboFX.Constants import SIDE


class LiveOrder(object):
    '''
    This class is an representation of a forex order
    '''
    def __init__(self, units, side, price, signals, trade_id):
        self.side = side
        self.units = units
        self.price = price
        self.cost = self.units * self.price
        self.duration = 288
        self.signals = signals
        self.trade_id = trade_id

    def jdefault(self, o):
        return o.__dict__

    def close(self, forexData):
        if self.side == 1:
            return (self.units*forexData['closeBid']) - self.cost
        elif self.side == -1:
            return (self.cost - (self.units * forexData['closeAsk']))

    def check_for_close(self, forexData):
        # check if the long order meets our criterias, and should stop
        self.duration -= 1

        if self.side == SIDE.LONG:
            if (self.units*forexData['closeBid']) - self.cost > 0:
                return self.trade_id
        elif self.side == SIDE.SHORT:
            if (self.cost - (self.units * forexData['closeAsk'])) > 0:
                return self.trade_id
        return 0
