'''
Created on 25/11/2014
@author: s103451
'''
import json
import nltk
from roboFX.Constants import SIDE


class FirstClassifier(object):
    '''
    This class performs the analasys of the data
    '''

    def __init__(self,
                 god_file_name="longList.txt",
                 bad_file_name="shortList.txt"):
        '''
        All of the OCHL data uses the bid prices
        '''
        self.count = 0

        # load examples of profitable trades
        godFile = open(god_file_name)
        self.godData = json.load(godFile)
        godFile.close()

        # load examples of trades with loss
        badFile = open(bad_file_name)
        self.badData = json.load(badFile)
        badFile.close()

        self.length = len(self.badData)
        if len(self.godData) > self.length:
            self.length = self.godData

    def features(self, example_order):
        return {"sma(10,40)": example_order["signals"]['sma(10,40)'],
                "rsi100": example_order["signals"]['rsi(100)'],
                "openBid": example_order["signals"]['openBid'],
                "closeBid": example_order["signals"]['closeBid'],
                "volume": example_order["signals"]['volume'],
                "spread": example_order["signals"]['spread'],
                }

    def train(self):
        featuresetLong = [(self.features(ind), 'long')
                          for ind in self.godData[0:self.length]]

        featuresetShort = [(self.features(ind), 'short')
                           for ind in self.badData[0:self.length]]

        self.classifier = nltk.NaiveBayesClassifier.train(featuresetLong +
                                                          featuresetShort)

    def analyse(self, signals):
        tmp = self.classifier.classify(signals)

        confidence = self.classifier.prob_classify(signals).prob(tmp)

        if confidence >= 0.85:
            if tmp == "long":
                return SIDE.LONG
            elif tmp == "short":
                return SIDE.SHORT
        else:
            return 0

    def show_most_informative_features(self):
        print self.classifier.show_most_informative_features(n=100)
