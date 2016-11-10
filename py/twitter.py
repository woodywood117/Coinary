#!/usr/bin python

import csv
import httplib

class twitterStruct(object):

    def __init__(self, url="test.com", date="1-1-1970"):
        self.currentData = None
        self.dataCounter = 0
        self.url = url
        self.date = date


    def gather(self, url, date):
            # Generate the connection to server
        conn = httplib.HTTPConnection(url)
            # Make request for specified date
        conn.request("GET", "/tweet_"+date)
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
            # Set the output
        self.currentData = output


    def nextTweet(self):
            # Asserts that you don't try to access data that there.
        if self.dataCounter > self.currentData.len():
            self.gather(self.url, self.date)
        return self.currentData[self.dataCounter]
