'''
Created on 28/10/2014
@author: s103451
'''
from roboFX2.LiveOrder import LiveOrder
from roboFX.Constants import SIDE
import json
import talib
import numpy as np
from oandapy import oandapy
import math


class LiveOrderManager(object):
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

        # variables to analyze fx_data
        '''
        All of the OCHL data uses the bid prices
        '''
        self.open = [None] * 100
        self.close = [None]*100
        self.high = [None]*100
        self.low = [None]*100
        self.volume = [None]*100

        self.oanda = oandapy.API(environment="practice",
                         access_token="e53fd8cfdb5f5e58c15f0936ece50939-4431fd4def9be7d92abb7ede43738eb4")
        self.accountID = 6774427

    def save_fx_data(self, fxData):
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
        self.save_fx_data(data)
        to_be_removed = []
        for order in self.orders:
            trade_id = order.check_for_close(data)

            if trade_id != 0:
                closeTrade = self.oanda.close_trade(account_id=self.accountID, trade_id=order.trade_id)
                profit = closeTrade['profit']
                self.account.deposit(profit+order.cost)
                to_be_removed.append(order)

        for order in to_be_removed:
            self.orders.remove(order)

    def get_signals(self):
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

    '''
    This method checks if two graphs have crossed
    and returns a value of
    1 if they have crossed and graphOne ends above
    -1 if they have crossed and graphOne ends below
    0 if they havn't crossed
    '''
    def crossing_graphs(self, graphOne1, graphOne2, GraphTwo1, GraphTwo2):
        if graphOne1 > GraphTwo1 and graphOne2 < GraphTwo2:
            return -1
        elif graphOne1 < GraphTwo1 and graphOne2 > GraphTwo2:
            return 1
        else:
            return 0

    def createOrder(self, side, data):
        if None not in self.open:
            amount = self.account.withdraw(side, data)

            if amount > 0:
                tmpSignals = self.get_signals()
                if side == SIDE.LONG:
                    self.account.deposit(amount)
                    '''
                    # place a buy order ask = immediate buy
                    trade = self.oanda.create_order(account_id=self.accountID,
                                                    instrument="EUR_USD", side="buy",
                                                    units=amount,
                                                    type="market"
                                                    )
                    self.orders.append(LiveOrder(side=SIDE.LONG,
                                                 units=amount,
                                                 price=data['closeAsk'],
                                                 signals=tmpSignals,
                                                 trade_id=trade['tradeOpened']['id']
                                                 )
                                       )'''
                if side == SIDE.SHORT:
                    # place a sell order bid = immediate sell

                    trade = self.oanda.create_order(account_id=self.accountID,
                                                    instrument="EUR_USD", side="sell",
                                                    units=amount,
                                                    type="market"
                                                    )
                    self.orders.append(LiveOrder(side=SIDE.SHORT,
                                                 units=amount,
                                                 price=trade['price'],
                                                 signals=tmpSignals,
                                                 trade_id=trade['tradeOpened']['id']
                                                 )
                                       )