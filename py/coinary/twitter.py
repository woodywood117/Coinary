#!/usr/bin python

import csv
import requests

class twitterStruct(object):

    def __init__(self, handle, url, date):
        self.currentData = None
        self.dataCounter = 0
        self.url = url
        self.date = date
        self.handle = handle


    def gather(self):
            # Download the next file
        req = requests.get(self.url+"/tweets/"+self.handle+"-"+self.date+".csv")
        if req.status_code != 200:
            print("File download error.")
            exit(1)
           # Convert data to CSV format
        cv = csv.reader(req.text.splitlines(), delimiter=',')
            # Convert CSV to list format
        cvl = list(cv)
            # Set the output
        self.currentData = cvl


    def nextTweet(self):
            # Asserts that you don't try to access data that there.
        if not self.currentData or self.dataCounter >= len(self.currentData):
            self.gather()
            self.dataCounter = 0
        ret = self.currentData[self.dataCounter]
        self.dataCounter = self.dataCounter + 1
        return ret
