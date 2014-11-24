'''
Created on 24/11/2014

@author: s103451
'''
import matplotlib.pyplot as plt
from roboFX.AccountManager import AccountManager
from roboFX.Constants import SIDE
from roboFX.DataStreaming import DataStreaming
from roboFX.OrderManager import OrderManager
from roboFX2.RandomTrader import RandomTrader


streamer = DataStreaming(filename="data.txt")
accountManager = AccountManager(10000)
manager = OrderManager(leverage=20, account=accountManager)

account_data = []
pair_data = []
signal_data = []

analyzer = RandomTrader()


for i in range(streamer.maxCount):
    tmp = streamer.getData()

    if i == (streamer.maxCount-1):
        manager.closeAllTrades(tmp)
    elif i != (streamer.maxCount-1):
        manager.update(tmp)

        signal = analyzer.analyse(tmp)

        if signal != 0:
            if signal == SIDE.SHORT:
                manager.createOrder(SIDE.SHORT, tmp)
            elif signal == SIDE.LONG:
                manager.createOrder(SIDE.LONG, tmp)

    account_data.append(accountManager.balance)
    pair_data.append(tmp['lowBid'])
    signal_data.append(signal)

manager.save_records()
print "Balance: "+str(accountManager.balance)
print "closed_profit: " + str(manager.getClosedProfit())
print "open_orders: "+str(manager.getNrOpenOrders())
plt.figure(1)
plt.subplot(211)
plt.plot(account_data)
plt.ylabel('account balance')
plt.subplot(212)
plt.plot(pair_data, color='green')
plt.ylabel('EUR/USD')

plt.show()
