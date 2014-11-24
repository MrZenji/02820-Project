'''
Created on 05/11/2014

@author: s103451
'''
from roboFX.DataStreaming import DataStreaming
from roboFX.RSIGenerator import RSIGenerator
from roboFX.ClassifyerGenerator import ClassifyerGenerator
from roboFX.OrderManager import OrderManager
from roboFX.AccountManager import AccountManager
import matplotlib.pyplot as plt
from roboFX.EAGenerator import EAGenerator
from roboFX.Constants import SIDE

streamer = DataStreaming(filename="data.txt")
analasys = RSIGenerator()
analasys2 = ClassifyerGenerator()
ea_analasys = EAGenerator()
accountManager = AccountManager(10000)
manager = OrderManager(leverage=20, account=accountManager)

account_data = []
pair_data = []
signal_data = []

# max 536252  length for fxdata.txt
# max 5000 length for data.txt


for _ in range(5000):
    tmp = streamer.getData()

    manager.update(tmp)

    signal = analasys.analyse(tmp)+analasys2.analyse(tmp)

    if signal != 0:
        if signal == 2:
            manager.createOrder(SIDE.LONG, tmp)
        elif signal == -2:
            manager.createOrder(SIDE.SHORT, tmp)

    account_data.append(accountManager.balance)
    pair_data.append(tmp['lowBid'])
    signal_data.append(signal)

print "account_balance(end): "+str(accountManager.balance)
plt.figure(1)
plt.subplot(211)
plt.plot(account_data)
plt.ylabel('account balance')
plt.subplot(212)
plt.plot(pair_data, color='green')
plt.ylabel('EUR/USD')

plt.show()
