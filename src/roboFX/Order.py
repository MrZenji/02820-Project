'''
Created on 28/10/2014
@param instrument: The currency pair being traded
@param units: The amount of valuta you would like to trade
@author: s103451
'''
from roboFX.Constants import SIDE


class Order(object):
    '''
    This class is an representation of a forex order
    '''
    def __init__(self, units, side, price, stopLoss, takeProfit, signals):
        self.side = side
        self.units = units
        self.price = price
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.cost = self.units * self.price
        self.duration = 288
        self.signals = signals

    def jdefault(self, obj):
        '''
        This method converts the object
        to JSON format
        '''
        return obj.__dict__

    def close(self, forexData):
        '''Closing an order'''
        if self.side == 1:
            return (self.units*forexData['closeBid']) - self.cost
        elif self.side == -1:
            return (self.cost - (self.units * forexData['closeAsk']))

    def check_for_close(self, forexData):
        '''
        Check if the order meets our criteria's,
        and should stop
        '''
        self.duration -= 1
        if self.side == SIDE.LONG:
            if forexData['lowBid'] >= self.takeProfit:
                return (self.units*self.takeProfit) - self.cost
            elif forexData['lowBid'] <= self.stopLoss:
                return (self.units*self.stopLoss) - self.cost
            elif self.duration <= 0:
                return (self.units*forexData['closeBid']) - self.cost
        elif self.side == SIDE.SHORT:
            # Close the order with profit
            if self.takeProfit >= forexData['highAsk']:
                return (self.cost - (self.units * self.takeProfit))
            elif self.stopLoss <= forexData['highAsk']:
                return (self.cost - (self.units * self.stopLoss))
            elif self.duration <= 0:
                return (self.cost - (self.units * forexData['closeAsk']))
        return 0
