#!/usr/bin python

import csv
import requests
import datetime

class twitterStruct(object):

    def __init__(self, handle, url, inDate):
        self.currentData = None
        self.dataCounter = 0
        self.url = url
        tmp = inDate.split(".")
        self.Date = datetime.date(int(tmp[2]),int(tmp[1]),int(tmp[0]))
        self.handle = handle


    def gather(self):
            # Download the next file
        req = requests.get(self.url+"/tweets/"+self.handle+"-"+self.Date.strftime("%d.%m.%Y")+".csv")
        d = datetime.timedelta(days=1)
        self.Date = self.Date + d
        if req.status_code != 200:
            print(req.status_code)
            print("Twitter file download error.\n"+self.url+"/tweets/"+self.handle+"-"+(self.Date - d).strftime("%d.%m.%Y")+".csv")
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
