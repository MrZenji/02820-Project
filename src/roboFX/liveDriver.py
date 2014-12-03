'''
Created on 24/11/2014

@author: s103451
'''
from oandapy import oandapy
import json

oanda = oandapy.API(environment="practice",
                    access_token="e53fd8cfdb5f5e58c15f0936ece50939-4431fd4def9be7d92abb7ede43738eb4")

# accountId = 6774427
#print json.dumps(oanda.get_account(6774427), indent=1)

fxData = oanda.get_history(instrument="EUR_USD", count=2)

print json.dumps(fxData, indent=1)

