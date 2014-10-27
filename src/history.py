'''
Created on 01/10/2014

@author: roboFX
'''

from oandapy import oandapy
import json

#accountId: 6774427
oanda = oandapy.API(environment="practice", access_token="2f96e09af1f5533df15c0b0c3849407d-358b90277196bad72701d707ddc0064f")

firstData = oanda.get_history(instrument="EUR_USD",granularity="M5",start="2007-10-01T18:00:00Z",count=5000)

history_data_file = open("fxdata.txt","a")

while(True):
    try:
        
        endTime = firstData["candles"][-1]["time"]

        getNextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=endTime,count=2)
        
        newStartTime = getNextData["candles"][-1]["time"]

        nextData = oanda.get_history(instrument="EUR_USD",granularity="M5",start=newStartTime,count=5000)
              
    except oandapy.OandaError:
        break

history_data_file.write(json.dumps(firstData["candles"],indent=1))
history_data_file.close()