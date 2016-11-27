#!/usr/bin python

import math

class tracker(object):

    def __init__(self):
        self.store = {}

    def addPair(self, word, value):
        if word not in self.store.keys():
            self.store[word] = []
        self.store[word].append(value)
