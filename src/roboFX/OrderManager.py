'''
Created on 28/10/2014
@author: s103451
'''
from roboFX.Order import Order


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
        # print "open trades: "+str(len(self.orders))
        for order in self.orders:
            profit = order.check_for_close(data)*self.leverage
            if profit != 0:
                self.account.deposit(profit)
                self.orders.remove(order)

    def createOrder(self, side, data):
        amount = self.account.withdraw()

        if amount > 0:
            if side == 1:
                # place a buy order ask = immediate buy

                self.orders.append(Order(side=1,
                                         units=(amount/data['closeAsk']),
                                         price=data['closeAsk'],
                                         stopLoss=data['closeAsk']*(1-0.0005),
                                         takeProfit=data['closeAsk']*1.0010))
                '''
                self.orders.append({'side': 1,
                                    'units': amount/data['closeAsk'],
                                    'price': data['closeAsk'],
                                    'stopLoss': data['closeAsk']*0.98,
                                    'takeProfit': data['closeAsk']*1.04})'''
            elif side == -1:
                # place a sell order bid = immediate sell
                self.orders.append(Order(side=-1,
                                         units=(amount/data['closeBid']),
                                         price=data['closeBid'],
                                         stopLoss=data['closeBid']*1.005,
                                         takeProfit=data['closeBid']*(1-0.001))
                                   )
                '''self.orders.append({'side': -1,
                                    'units': amount/data['closeBid'],
                                    'price': data['closeBid'],
                                    'stopLoss': data['closeBid']*1.04,
                                    'takeProfit': data['closeBid']*0.92})'''

    def getClosedProfit(self, period):
        return self.profit
