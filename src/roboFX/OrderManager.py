'''
Created on 28/10/2014
@author: s103451
'''
from roboFX.Order import Order
from roboFX.Constants import SIDE
import json
import talib
import numpy as np


class OrderManager(object):
    '''
    This class is responsible to execute and update
    the orders depending on the market and the orderType
    '''
    def __init__(self, leverage, account):
        self.leverage = leverage
        self.account = account
        self.orders = []
        self.profit = 0
        self.records = {"longOrders": [], "shortOrders": []}

        # variables to analyze fx_data
        '''
        All of the OCHL data uses the bid prices
        '''
        self.open = [None] * 100
        self.close = [None]*100
        self.high = [None]*100
        self.low = [None]*100
        self.volume = [None]*100

    def save_fx_data(self, fxData):
        '''Saves current data that is retrieved'''
        self.open.pop(0)
        self.open.append(fxData['openBid'])
        self.close.pop(0)
        self.close.append(fxData['closeBid'])
        self.high.pop(0)
        self.high.append(fxData['highBid'])
        self.low.pop(0)
        self.low.append(fxData['lowBid'])
        self.volume.pop(0)
        self.volume.append(fxData['volume'])

    def update(self, data):
        '''Updating orders and closing orders'''
        self.save_fx_data(data)
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

    def get_signals(self):
        '''Creating signals'''
        # First Classifier Signals
        rsi_100 = talib.RSI(np.array(self.close), timeperiod=99)[-1]
        sma_101 = talib.SMA(np.array(self.close), timeperiod=10)[-1]
        sma_102 = talib.SMA(np.array(self.close), timeperiod=10)[-2]
        sma_401 = talib.SMA(np.array(self.close), timeperiod=40)[-1]
        sma_402 = talib.SMA(np.array(self.close), timeperiod=40)[-2]

        # Second Classifier Signals
        open_bid = self.open[-1]
        close_bid = self.close[-1]
        volume = self.volume[-1]
        # The volatility of the market within 5-minutes
        spread = self.high[-1]-self.low[-1]

        # Third Classifier Signals
        macd = talib.MACD(np.array(self.close))[-1][-1]

        sar = talib.SAR(np.array(self.high), np.array(self.low))[-1]

        return {"rsi(100)": rsi_100,
                "sma(10,40)": self.crossing_graphs(sma_102, sma_101,
                                                   sma_402, sma_401),
                "openBid": open_bid,
                "closeBid": close_bid,
                "volume": volume,
                "spread": spread,
                "macd_signal": macd,
                "sar": sar
                }

    def crossing_graphs(self, firstGraphOne, secondGraphOne,
                        firstGraphTwo, secondGraphTwo):
        '''
        This method checks if two graphs have crossed
        and returns a value of
        1 if they have crossed and firstGraphOne ends above,
        -1 if they have crossed and secondGraphOne ends below
        0 if they havn't crossed
        '''
        if firstGraphOne > firstGraphTwo and secondGraphOne < secondGraphTwo:
            return -1
        elif firstGraphOne < firstGraphTwo and secondGraphOne > secondGraphTwo:
            return 1
        else:
            return 0

    def createOrder(self, side, data):
        '''This method creates an order'''
        if None not in self.open:
            amount = self.account.withdraw()
            if amount > 0:
                if side == SIDE.LONG:
                    # place a buy order ask = immediate buy
                    self.orders.append(Order(side=SIDE.LONG,
                                             units=(amount/data['closeAsk']),
                                             price=data['closeAsk'],
                                             stopLoss=data['lowBid']*(1-0.0005),
                                             takeProfit=data['closeAsk']*1.0010,
                                             signals=self.get_signals()
                                             )
                                       )
                elif side == SIDE.SHORT:
                    # place a sell order bid = immediate sell
                    self.orders.append(Order(side=SIDE.SHORT,
                                             units=(amount/data['closeBid']),
                                             price=data['closeBid'],
                                             stopLoss=data['highAsk']*1.005,
                                             takeProfit=data['closeBid']*(1-0.0010),
                                             signals=self.get_signals()
                                             )
                                       )

    def record_order(self, order, profit):
        '''
        If an order makes profit,
        save it for record keeping
        '''
        if profit > 0:
            if order.side == SIDE.LONG:
                self.records["longOrders"].append(order)
            elif order.side == SIDE.SHORT:
                self.records["shortOrders"].append(order)

    def getClosedProfit(self):
        '''Returning closed profit'''
        return self.profit

    def getNrOpenOrders(self):
        '''Returning number of open orders'''
        return len(self.orders)

    def closeAllTrades(self, data):
        '''Closes all open trades'''
        for order in self.orders:
            profit = order.close(data)*self.leverage
            cost = order.cost

            self.profit += profit
            self.account.deposit(profit+cost)
            self.record_order(order, profit)

        self.orders = []

    def save_records(self):
        '''Saves all the recorded orders to files'''
        with open("longList.txt", 'w') as proFile:
            output = "["
            for order in self.records['longOrders']:
                output += json.dumps(order, default=order.jdefault,
                                     indent=1)+","
            output = output[0:-1]+"]"
            proFile.write(output)

        with open("shortList.txt", 'w') as lossFile:
            output = "["
            for order in self.records['shortOrders']:
                output += json.dumps(order, default=order.jdefault,
                                     indent=1)+","
            output = output[0:-1]+"]"
            lossFile.write(output)
