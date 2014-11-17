'''
Created on 28/10/2014
@param instrument: The currency pair being traded
@param units: The amount of valuta you would like to trade
@author: s103451
'''


class Order(object):
    '''
    This class is an representation of a forex order
    '''
    def __init__(self, units, side, price, stopLoss, takeProfit):
        self.side = side
        self.units = units
        self.price = price
        self.stopLoss = stopLoss
        self.takeProfit = takeProfit
        self.cost = self.units * self.price

    def check_for_close(self, forexData):
        # check if the long order meets our criterias, and should stop
        if self.side == 1:
            if forexData['lowAsk'] < self.takeProfit < forexData['highAsk']:
                # print "long - profit"
                return (self.units*self.takeProfit)-self.cost
            elif forexData['lowAsk'] < self.stopLoss < forexData['highAsk']:
                # print "long - loss"
                return (self.units*self.stopLoss)-self.cost
        elif self.side == -1:
            # Close the order with profit
            if forexData['lowBid'] < self.takeProfit < forexData['highBid']:
                # print "short - profit["
                # print str(self.cost-self.takeProfit*self.units+self.cost)+":"+str(self.cost)+"]"
                return (self.cost - (self.units * self.takeProfit)) + self.cost
            # Close the order with a acceptable loss
            elif forexData['lowBid'] < self.stopLoss < forexData['highBid']:
                # print "short - lose"
                return (self.cost - (self.units * self.stopLoss)) + self.cost

        return 0
