'''
Created on 08/10/2014

@author: Kevin V. Sjøbeck
'''

class Order(object):
    '''
    This class contains all the details regarding the order
    
    Direction enum:
    Long =   1
    Short = -1
    '''

    def __init__(self, stop,profit,price, amount, direction):        
        self.stop = stop
        self.direction = direction
        self.profit = profit
        self.price = price
        self.amount = amount


    def close(self,OCHL):
        if self.direction == 1:
            self.closePrice = OCHL['highBid']
        elif self.direction == -1:
            self.closePrice = OCHL['lowAsk']