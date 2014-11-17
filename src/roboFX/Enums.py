'''
Created on 17/11/2014

@author: Kevin
This class is used to comprehend with the fact, that python 2.7
doesn't come with enums, as default
'''


def enum(**enums):
    return type('Enum', (), enums)
