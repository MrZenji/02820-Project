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

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self):
        if self.balance > 2:
            tmp = self.balance * 0.02
            self.balance -= self.balance*0.02
            return tmp
        else:
            return 0
