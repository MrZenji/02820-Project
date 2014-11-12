'''
Created on 12/11/2014

@author: s103451
'''
import unittest
from roboFX.Order import Order


class TestOrder(unittest.TestCase):

    def setUp(self):
        # FOREX test data
        self.forexData = {"highAsk": 1.2955, "lowAsk": 1.29524,
                          "complete": True,
                          "openBid": 1.2953, "closeAsk": 1.29545,
                          "closeBid": 1.29532, "volume": 20,
                          "openAsk": 1.29543,
                          "time": "2014-09-08T00:10:00.000000Z",
                          "lowBid": 1.29511, "highBid": 1.29537}
        self.orders = []
        self.orders.append(Order(side=1, units=2, price=1.2935,
                                 stopLoss=1.2935*0.96, takeProfit=1.2935*1.08))

        self.assertEqual(first=1, second=len(self.orders))

        self.orders.append(Order(side=-1, units=2, price=1.2935,
                                 stopLoss=1.2935*1.04, takeProfit=1.2935*0.92))

        self.assertEqual(first=2, second=len(self.orders))

    def test_closeLongOrder(self):
        # test to see that none of the orders gets closed on the default data
        for o in self.orders:
            self.assertEqual(0, o.check_for_close(self.forexData))

        # test to check that it is possible to close a long order,
        # with positive profit
        self.forexData['highAsk'] = 1.4980
        self.assertEqual(0.20696000000000003,
                         self.orders[0].check_for_close(self.forexData))

        # test to check that it is possible to close a long order,
        # with a negative loss
        self.forexData['highAsk'] = 1.2955
        self.forexData['lowAsk'] = 1.2396

        self.assertEqual(-0.10348000000000024,
                         self.orders[0].check_for_close(self.forexData))

    def test_closeShortOrder(self):
        # test to check that the short order, don't close,
        # at the wrong time
        self.forexData['highAsk'] = 1.4980
        self.assertEqual(0,
                         self.orders[1].check_for_close(self.forexData))

        self.forexData['highAsk'] = 1.2955
        self.forexData['lowAsk'] = 1.2396

        self.assertEqual(0,
                         self.orders[1].check_for_close(self.forexData))

        # Test to see if, we it is possible to get a negative profit,
        # on a short order
        self.forexData['highBid'] = 1.4980
        self.assertEqual(-0.10348000000000024,
                         self.orders[1].check_for_close(self.forexData))

        self.forexData['highBid'] = 1.2955
        self.forexData['lowBid'] = 1.1896

        # test if it is possible to close a short order, with a
        # positive profit
        self.assertEqual(0.20696000000000003,
                         self.orders[1].check_for_close(self.forexData))

if __name__ == '__main__':
    unittest.main()
