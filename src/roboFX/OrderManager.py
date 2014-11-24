'''
Created on 28/10/2014
@author: s103451
'''
from roboFX.Order import Order
from roboFX.Constants import SIDE
import json


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
        self.profit = 0
        self.records = {"profitOrders": [], "lossOrders": []}

    def update(self, data):
        to_be_removed = []
        for order in self.orders:
            profit = order.check_for_close(data)*self.leverage
            cost = order.cost

            if profit != 0:
                self.profit += profit
                self.account.deposit(profit+cost)
                to_be_removed.append(order)
                self.record_order(order, profit)

        for order in to_be_removed:
            self.orders.remove(order)

    def createOrder(self, side, data):
        amount = self.account.withdraw()

        if amount > 0:

            if side == SIDE.LONG:
                # place a buy order ask = immediate buy
                self.orders.append(Order(side=SIDE.LONG,
                                         units=(amount/data['closeAsk']),
                                         price=data['closeAsk'],
                                         stopLoss=data['lowBid']*(1-0.0005),
                                         takeProfit=data['closeAsk']*1.0010))
            elif side == SIDE.SHORT:
                # place a sell order bid = immediate sell
                self.orders.append(Order(side=SIDE.SHORT,
                                         units=(amount/data['closeBid']),
                                         price=data['closeBid'],
                                         stopLoss=data['highAsk']*1.005,
                                         takeProfit=data['closeBid']*(1-0.0010)
                                         )
                                   )

    def record_order(self, order, profit):
        if profit > 0:
            self.records["profitOrders"].append(order)
        elif profit < 0:
            self.records["lossOrders"].append(order)

    def getClosedProfit(self):
        return self.profit

    def getNrOpenOrders(self):
        return len(self.orders)

    def closeAllTrades(self, data):
        for order in self.orders:
            profit = order.close(data)*self.leverage
            cost = order.cost

            self.profit += profit
            self.account.deposit(profit+cost)
            self.record_order(order, profit)

        self.orders = []

    def save_records(self):
        with open("profitList.txt", 'w') as proFile:
            output = "["
            for order in self.records['profitOrders']:
                output += json.dumps(order, default=order.jdefault,
                                     indent=1)+","
            output = output[0:-1]+"]"
            proFile.write(output)

        with open("lossList.txt", 'w') as lossFile:
            output = "["
            for order in self.records['lossOrders']:
                output += json.dumps(order, default=order.jdefault,
                                     indent=1)+","
            output = output[0:-1]+"]"
            lossFile.write(output)
