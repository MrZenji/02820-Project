'''
Created on 28/10/2014

@author: Kevin
'''


class AccountManager(object):
    '''
    This class is responsible to manage the
    account balance and managing the risk, in order
    to insure that you don't lose everything all
    at once.
    '''
    def __init__(self, startbalance):
        self.balance = startbalance

    def getBalance(self):
        return self.balance

    def withdraw(self):
        return self.balance*0.3
