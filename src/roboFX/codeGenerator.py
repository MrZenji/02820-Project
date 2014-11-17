'''
Created on 05/11/2014

@author: s103451
'''
from roboFX.DataStreaming import DataStreaming
from roboFX.RSIGenerator import RSIGenerator
from roboFX.OrderManager import OrderManager
from roboFX.AccountManager import AccountManager
import matplotlib.pyplot as plt
from roboFX.EAGenerator import EAGenerator


streamer = DataStreaming(filename="data.txt")
analasys = RSIGenerator()
ea_analasys = EAGenerator()
accountManager = AccountManager(10000)
manager = OrderManager(leverage=1, account=accountManager)

account_data = []
pair_data = []
signal_data = []


# max 536252  length for fxdata.txt
# max 5000 length for data.txt
for _ in range(300):
    tmp = streamer.getData()
    manager.update(tmp)
    ea_analasys.analyse(tmp)
    signal = analasys.analyse(tmp)

    if signal != 0:
        manager.createOrder(signal, tmp)

    account_data.append(accountManager.balance)
    pair_data.append(tmp['lowBid'])
    signal_data.append(signal)

plt.figure(1)
plt.subplot(211)
plt.plot(account_data)
plt.ylabel('account balance')
plt.subplot(212)
plt.plot(pair_data, color='green')
plt.ylabel('EUR/USD')

plt.show()
