'''
Created on 01/10/2014

@author: station
'''



def signal(data):
    longs = 0
    shorts = 0
    last = 0
    for d in data:
        if last == 0:
            last = d
        elif d > last:
            longs+=1
        elif d < last:
            shorts+=1
        
        last = d
    
    RS = 0
    if shorts == 0:
        RS = longs
    else:
        RS = longs/shorts
    
    result = 100 - 100/(1+RS)
    
    if result > 70:
        return -1
    elif result < 30:
        return 1
    else:
        return 0 