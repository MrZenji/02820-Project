'''
Created on 28/10/2014
@author: s103451
'''
from roboFX.Chromosome import Chromosome
from roboFX.Constants import OPERATOR
from random import randint
from roboFX.OrderManager import OrderManager
from roboFX.AccountManager import AccountManager
import copy


class EAGenerator(object):
    '''
    This class performs the analasys of the data, using
    Evolutionary Algorithm approach on financial data
    '''

    def __init__(self):
        '''
        All of the OCHL data uses the bid prices
        '''
        self.open = [None] * 200
        self.close = [None]*200
        self.high = [None]*200
        self.low = [None]*200
        self.volume = [None]*200

        # Manager to be used in the fitness test of the algorithm
        self.manager = OrderManager(account=AccountManager(10000), leverage=1)

        # the data to be used during fitness test comparison
        self.dna_closed_profit = 0
        self.tmp_dna_closed_profit = 0

        # The dna sequence of the generator
        self.dna = [None]

        self.tmp_dna = [Chromosome(technical_indicator=0,
                                   period=100,
                                   operator=OPERATOR.GTE,
                                   expected_value=30),
                        Chromosome(technical_indicator=0,
                                    period=100,
                                    operator=OPERATOR.LSE,
                                    expected_value=70)]

    def analyse(self, data):
        self.open.pop(0)
        self.open.append(data['openBid'])
        self.close.pop(0)
        self.close.append(data['closeBid'])
        self.high.pop(0)
        self.high.append(data['highBid'])
        self.low.pop(0)
        self.low.append(data['lowBid'])
        self.volume.pop(0)
        self.volume.append(data['volume'])

        signal_indicator = 0

        for chrome in self.dna:
            if chrome.signal():
                signal_indicator += 1

        if signal_indicator >= len(self.dna)/2:
            return 1
        else:
            return 0

    def mutate(self):
        # Give 1/n'th chance of mutating the different chromosones.
        for chrome in self:
            if randint(0, len(self.dna)) == 1:
                chrome.mutate()

    def fitness(self):
        if self.tmp_dna_closed_profit > self.dna_closed_profit:
            self.dna_closed_profit = self.tmp_dna_closed_profit
            self.dna = copy.deepcopy(self.tmp_dna)
