'''
Created on 24/11/2014

@author: s103451
'''
from random import randrange
from roboFX.Constants import SIDE


class RandomTrader(object):
    '''
    This class simulates a person who trades randomly
    '''

    def analyse(self, data):
        i = randrange(10)

        if i == 0:
            return SIDE.SHORT
        elif i == 1:
            return SIDE.LONG
        else:
            return 0
