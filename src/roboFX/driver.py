'''
Created on 24/11/2014

@author: s103451

This is our driver that runs
the back testing program
'''
import matplotlib.pyplot as plt
from roboFX.AccountManager import AccountManager
from roboFX.Constants import SIDE
from roboFX.DataStreaming import DataStreaming
from roboFX.OrderManager import OrderManager
from roboFX.RandomTrader import RandomTrader
from roboFX.Classifier import Classifier


streamer = DataStreaming(filename="data.txt")
accountManager = AccountManager(10000)
manager = OrderManager(leverage=20, account=accountManager)

account_data = []
pair_data = []

# analyzer = RandomTrader()
analyzer = Classifier(conf_intval=0.96)
analyzer.train()
# analyzer.show_most_informative_features()

for i in range(streamer.maxCount):
    tmp = streamer.getData()
    manager.update(tmp)
    if i == (streamer.maxCount-1):
        manager.closeAllTrades(tmp)
    elif i != (streamer.maxCount-1) and i >= 100:
        signal = analyzer.analyse(tmp)

        if signal != 0:
            if signal == SIDE.SHORT:
                manager.createOrder(SIDE.SHORT, tmp)
            elif signal == SIDE.LONG:
                manager.createOrder(SIDE.LONG, tmp)

    account_data.append(manager.getClosedProfit())
    pair_data.append(tmp['lowBid'])

# manager.save_records()
'''Print out result data'''
print "Balance: "+str(accountManager.balance)
print "closed_profit: " + str(manager.getClosedProfit())
print "open_orders: "+str(manager.getNrOpenOrders())
plt.figure(1)
plt.subplot(211)
plt.plot(account_data)
plt.ylabel('closed profit')
plt.subplot(212)
plt.plot(pair_data, color='green')
plt.ylabel('EUR/USD')

plt.show()
