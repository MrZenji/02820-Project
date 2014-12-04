'''
Created on 17/11/2014

@author: Kevin
'''


def enum(**enums):
    '''
    This class is used to comprehend with the fact,
    that python 2.7 doesn't come with enums, as default
    '''
    return type('Enum', (), enums)
