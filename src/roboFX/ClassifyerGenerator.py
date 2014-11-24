'''
Created on 19/11/2014

@author: Kevin
'''
'''
Created on 28/10/2014
@author: s103451
'''
import nltk
import random
import json
from roboFX.Constants import SIDE

class ClassifyerGenerator(object):
    '''
    This class performs the analasys of the data
    '''

    def __init__(self):
        '''
        All of the OCHL data uses the bid prices
        '''
        self.last_exchange_rate = 0
        self.tmp_data = [None]*10

        featureset = [(self.features(json.loads(ind)), 'long') for (ind) in open("long.txt")]+[(self.features(json.loads(ind)), 'short') for (ind) in open("short.txt")]
        random.shuffle(featureset)
        train_set, test_set = featureset[500:], featureset[:500]
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)
        print "accuracy: "+str(nltk.classify.accuracy(self.classifier,test_set))

    def features(self, ind):
        count_positive = 0
        count_negative = -1
        for n in ind:
            if n == 1:
                count_positive += 1
            elif n == -1:
                count_negative += -1
        return {"Sum": sum(ind), "Count_positive": count_positive, "Count_negative": count_negative}

    def analyse(self, data):

        if self.last_exchange_rate == 0:
            self.last_exchange_rate = data['closeBid']
        else:
            if data['closeBid'] > self.last_exchange_rate:
                self.tmp_data.pop(0)
                self.tmp_data.append(1)
            elif data['closeBid'] < self.last_exchange_rate:
                self.tmp_data.pop(0)
                self.tmp_data.append(-1)

        if None not in self.tmp_data:
            side = self.classifier.classify(self.features(self.tmp_data))

            if side == "long":
                return SIDE.LONG
            elif side == "short":
                return SIDE.SHORT

        return 0
