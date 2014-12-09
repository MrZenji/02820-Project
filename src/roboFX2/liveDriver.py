'''
Created on 04/12/2014

@author: Kevin
'''
import time

from roboFX2.LiveAccountManager import LiveAccountManager
from roboFX.Constants import SIDE
from roboFX.FirstClassifier import FirstClassifier
from roboFX2.LiveOrderManager import LiveOrderManager
from roboFX2.LiveStreaming import LiveStreaming


streamer = LiveStreaming(granularity="S5")
accountManager = LiveAccountManager(10000)
manager = LiveOrderManager(leverage=50, account=accountManager)

analyzer = FirstClassifier()
analyzer.train()
count = 0
while True:
    tmp = streamer.getData()

    manager.update(tmp)
    print str(count)

    if count >= 100:
        signal = analyzer.analyse(tmp)

        if signal != 0:
            if signal == SIDE.SHORT:
                manager.createOrder(SIDE.SHORT, tmp)
                print "Short Order"
            elif signal == SIDE.LONG:
                manager.createOrder(SIDE.LONG, tmp)
                print "long Order"

    count += 1
    time.sleep(5)
