'''
Created on 28/10/2014
@author: Kevin
'''


class OrderManager(object):
    '''
    This class is responsible to execute and update
    the orders depending on the market and the orderType
    This class is also responsible to manage the profibility
    of the current strategy.
    '''
    def __init__(self, leverage, account):
        self.leverage = leverage
        self.account = account

    def update(self):
        print "update"

    def createOrder(self, instrument, side):
        units = self.account.withdraw()

        if units > 0:
            print "place an order"+side

    def getClosedProfit(self, period):
        return self.profit
