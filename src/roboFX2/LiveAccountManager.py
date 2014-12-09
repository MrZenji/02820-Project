'''
Created on 28/10/2014

@author: Kevin
'''
from roboFX.Constants import SIDE


class LiveAccountManager(object):
    '''
    This class is responsible to manage the
    account balance and managing the risk, in order
    to insure that you don't lose everything all
    at once.
    '''
    def __init__(self, startbalance):
        self.balance = startbalance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, side, data):
        if self.balance > 2:
            if side == SIDE.LONG:
                tmp = self.balance * 0.02
                units = int((tmp/data['closeAsk']))
                self.balance -= units
                return units
            elif side == SIDE.SHORT:
                tmp = self.balance * 0.02
                units = int((tmp/data['closeAsk']))
                self.balance -= units
                return units
        else:
            return 0
