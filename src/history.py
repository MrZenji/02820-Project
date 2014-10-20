'''
Created on 01/10/2014

@author: station
'''

import oandapy.oandapy as oandapy
import json
import indicators.rsi as rsi
import indicators.sr as sr 
import matplotlib.pyplot as plt

#accountId: 6774427
oanda = oandapy.API(environment="practice", access_token="2f96e09af1f5533df15c0b0c3849407d-358b90277196bad72701d707ddc0064f")

firstData = oanda.get_history(instrument="EUR_USD",granularity="M5",start="2007-10-01T18:00:00Z",count=5000)
'''
endTime = firstData["candles"][-1].__getitem__("time")

getNextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=endTime,count=2)

newStartTime = getNextData["candles"][-1].__getitem__("time")

nextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=newStartTime,count=5000)

print json.dumps(firstData["candles"][-1],indent=1)
print json.dumps(nextData["candles"][0],indent=1)
'''

history_data_file = open("fxdata.txt","a")

while(True):
    try:
        
        endTime = firstData["candles"][-1].__getitem__("time")

        getNextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=endTime,count=2)
        
        newStartTime = getNextData["candles"][-1].__getitem__("time")

        nextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=newStartTime,count=5000)
              
    except oandapy.OandaError:
        break

history_data_file.write(json.dumps(firstData["candles"],indent=1))
history_data_file.close()

'''
account_balance = 100

json_data=open('data.txt')
data = json.load(json_data)
json_data.close()

tmp = [0]*14


bought_price= 0

data_account = []
data_instrument = []

amount = 2

for t in data["candles"]:
    tmp.pop(0)
    tmp.append(t["closeBid"])
    data_account.append(account_balance)
    data_instrument.append(t["closeBid"]) 
        
    signal = sr.signal(tmp)     
    signal = rsi.signal(tmp)
    
    if signal == 1:        
        if bought_price == 0:
            if account_balance > t["closeBid"]*amount:
                bought_price = t["closeBid"]
                account_balance -= t["closeBid"]*amount
        elif bought_price > 0:
            account_balance += t["closeBid"]*amount
            bought_price = 0         
    elif signal == -1:
        if bought_price == 0:
            if account_balance > t["closeBid"]*amount:
                bought_price = t["closeBid"]
                account_balance -= t["closeBid"]*amount
        elif bought_price > 0:
            account_balance += (bought_price-t["closeBid"])*amount
            bought_price = 0
            
    


print account_balance

plt.figure(1)
plt.text(100, 20, "Buy signal")
plt.plot(data_account,color="green")
plt.figure(2)
plt.plot(data_instrument)
plt.ylabel('some numbers')
plt.show()
'''