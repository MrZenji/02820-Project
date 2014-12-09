'''
Created on 09/12/2014

@author: Sabrije
'''

import json
import talib
import numpy as np
from oandapy import oandapy
import math

oandaAC = oandapy.API(environment="practice",
                         access_token="657af47e3c2b562c6baae594e407a961-60cf041ddb3bc253b4c23acb23794f1e")


#print json.dumps(oandaAC.get_accounts(), indent=1)
accountId = oandaAC.get_accounts()
print accountId["accounts"][0]["accountId"]