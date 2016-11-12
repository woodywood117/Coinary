#!/usr/bin python

import csv
import requests

class stockStruct(object):

    def __init__(self, symbol, url, date):
        self.currentData = None
        self.dataCounter = 0
        self.url = url
        self.date = date
        self.symbol = symbol


    def gather(self):
            # Download the next file
        req = requests.get(self.url+"/stocks/"+self.symbol+"-"+self.date+".csv")
        if req.status_code != 200:
            print("File download error.")
            exit(1)
            # Convert data to CSV format
        cv = csv.reader(req.text.splitlines(), delimiter=',')
            # Convert CSV to list format
        cvl = list(cv)
            # Set the output
        self.currentData = cvl


    def nextVal(self):
            # Asserts that you don't try to access data that there.
        if not self.currentData or self.dataCounter >= len(self.currentData):
            self.gather()
            self.dataCounter = 0
        ret = self.currentData[self.dataCounter]
        self.dataCounter = self.dataCounter + 1
        return ret
