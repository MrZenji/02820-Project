'''
Created on 17/11/2014

@author: Kevin
@param Technical Indicator(TI):
@param period:
@param operator:
@param expected value:
@return signal:

A Chromosome, is a description of a specific
    Technical indicator, as well as it's parameters
    that are being used to define an Evolutionary Algorithm,
    it will raise a signal that can either be True or False,
    depending on the parameters passed to the Chromosome.
'''


class Chromosome(object):
    def __init__(self, technical_indicator, period, operator, expected_value):
        self.technical_indicator = technical_indicator
        self.period = period
        self.operator = operator
        self.expected_value = expected_value

    def mutate(self):
        print "mutate"

    def signal(self):
        return False
