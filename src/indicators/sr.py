'''
Created on 02/10/2014

@author: station
'''



def signal(data):   
    
    
    for d in data:
        if d < signal.support:
            signal.support = d
            return 1
        elif d > signal.ressistance:
            signal.ressistance = d
            return -1
         
    return 0

signal.support = 0
signal.ressistance = 0