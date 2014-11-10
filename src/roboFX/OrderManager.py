'''
Created on 28/10/2014
@author: s103451
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
        self.orders = []

    def update(self, data):
        for order in self.orders:
            if order['side'] == 1:
                # check for if we should close an buy order
                if order['takeProfit'] >= data['highBid']:
                    self.account.deposit(order['units']*data['highBid'])
                    self.orders.remove(order)
                elif order['stopLoss'] <= data['highBid']:
                    self.account.deposit(order['units']*data['highBid'])
                    self.orders.remove(order)
            elif order['side'] == -1:
                # check for if we should close an sell order
                if order['takeProfit'] >= data['highAsk']:
                    self.account.deposit(order['units']*data['highAsk'])
                    self.orders.remove(order)
                elif order['stopLoss'] <= data['highAsk']:
                    self.account.deposit(order['units']*data['highAsk'])
                    self.orders.remove(order)

    def createOrder(self, side, data):
        amount = self.account.withdraw()

        if amount > 0:
            # print "place an order: "+str(side)
            if side == 1:
                # place a buy order ask = immediate buy
                self.orders.append({'side': 1,
                                    'units': amount/data['closeAsk'],
                                    'price': data['closeAsk'],
                                    'stopLoss': data['closeAsk']*0.96,
                                    'takeProfit': data['closeAsk']*1.10})
            elif side == -1:
                # place a sell order bid = immediate sell
                self.orders.append({'side': -1,
                                    'units': amount/data['closeBid'],
                                    'price': data['closeBid'],
                                    'stopLoss': data['closeBid']*0.96,
                                    'takeProfit': data['closeBid']*1.12})

    def getClosedProfit(self, period):
        return self.profit
