'''
Created on 02/10/2014

@author: Kevin V. Sjøbeck
'''

class Manager(object):
    '''
    The manager will be responsible for selling and buying all of
    your 3-way orders after you placed an order
    '''
    
    def __init__(self, balance):
        self.orders = []
        self.balance = balance
        
    def place_order(self, order):
        self.orders.append(order)
        
    def sell_order(self,order):
        self.orders.remove(order)
        
        return (order.price-order.closePrice)*order.amount
        
        
    def update(self,OCHL):        
        if len(self.orders) > 0:
            for order in self.orders:
                order.close(OCHL)
                self.sell_order(order) 