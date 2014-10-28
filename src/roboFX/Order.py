'''
Created on 28/10/2014
@param instrument: The currency pair being traded
@param units: The amount of valuta you would like to trade
@author: Kevin
'''


class Order(object):
    '''
    This class is an representation of a forex order
    '''
    def __init__(self, instrument, units, side, orderType, expiry, price, stopLoss, takeProfit):
        self.instrument = instrument
        self.units = units
        self.orderType = orderType
        self.expiry = expiry
        self.price = price
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
