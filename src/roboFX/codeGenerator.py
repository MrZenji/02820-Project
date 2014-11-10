'''
Created on 05/11/2014

@author: s103451
'''
from roboFX.DataStreaming import DataStreaming
from roboFX.SignalGenerator import SignalGenerator
from roboFX.OrderManager import OrderManager
from roboFX.AccountManager import AccountManager
import matplotlib.pyplot as plt


streamer = DataStreaming()
analasys = SignalGenerator()
accountManager = AccountManager(1000)
manager = OrderManager(leverage=1, account=accountManager)

data = []
pair = []
trades = []
for i in range(5000):
    tmp = streamer.getData()
    manager.update(tmp)
    signal = analasys.analyse(tmp)

    if signal != 0:
        manager.createOrder(signal, tmp)

    data.append(accountManager.balance)
    pair.append(tmp['lowBid'])

plt.figure(1)
plt.subplot(211)
plt.plot(data)
plt.ylabel('account balance')
plt.subplot(212)
plt.plot(pair, color='green')
plt.ylabel('EUR/USD')

plt.show()
