#!/usr/bin python

import csv
import httplib

class stockStruct(object):

    def __init__(self, url = "test.com", date = "1.1.1970", symbol):
        self.currentData = None
        self.dataCounter = 0
        self.url = url
        self.date = date
        self.name = symbol


    def gather(self, url, date):
            # Generate the connection to server
        conn = httplib.HTTPConnection(url)
            # Make request for specified date
        conn.request("GET", "/stock-"+self.symbol+"-"+date+".csv")
            # Read the response from the socket
        resp = conn.getresponse()
            # Check that we got a response
        if resp.status != 200:
                # If we didn't, return error code
            return resp.status
            # Process the request
        output = resp.read()
            # Close the connection
        conn.close()
            # Convert data to CSV format
        cv = csv.reader(output.splitlines(), delimiter=',')
            # Convert CSV to list format
        cvl = list(cv)
            # Set the output
        self.currentData = cvl


    def nextVal(self):
            # Asserts that you don't try to access data that there.
        if not self.currentData or self.dataCounter >= len(self.currentData):
            self.gather(self.url, self.date)
            self.dataCounter = 0
        ret = self.currentData[self.dataCounter]
        self.dataCounter = self.dataCounter + 1
        return ret
